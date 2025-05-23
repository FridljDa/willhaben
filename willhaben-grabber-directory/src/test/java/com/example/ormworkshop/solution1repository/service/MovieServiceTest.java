package com.example.ormworkshop.solution1repository.service;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.junit.jupiter.params.provider.Arguments.arguments;

import java.math.BigDecimal;
import java.util.Set;
import java.util.stream.Stream;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.dao.DataIntegrityViolationException;

import com.example.ormworkshop.solution1repository.datamodel.Movie;

@SpringBootTest
class MovieServiceTest {
    @Autowired
    private MovieService movieService;

    @Test
    void should_persist_a_movie_to_the_database() {
        // given
        String movieName = "some name";
        int year = 2016;
        BigDecimal price = BigDecimal.ONE;

        // when
        long movieCountBeforePersisting = movieService.countMovies();
        Movie persistedMovie = movieService.persistMovieInDB(movieName, year, price);
        long movieCountAfterPersisting = movieService.countMovies();

        // then
        assertThat(persistedMovie).isNotNull();
        assertThat(persistedMovie.getName()).isEqualTo(movieName);
        assertThat(movieCountAfterPersisting).isEqualTo(movieCountBeforePersisting + 1);
    }

    @Test
    void should_retrieve_a_movie_by_id() {
        // given
        String movieName = "some name";
        int year = 2016;
        BigDecimal price = BigDecimal.ONE;

        // when
        Movie persistedMovie = movieService.persistMovieInDB(movieName, year, price);
        assertThat(persistedMovie).isNotNull();

        Movie movieFoundById = movieService.findMovieById(persistedMovie.getId());

        // then
        assertThat(persistedMovie.getId()).isNotNull();
        assertThat(movieFoundById).usingRecursiveComparison().ignoringFields("price").isEqualTo(persistedMovie);
    }

    @Test
    void should_retrieve_a_movie_by_name() {
        // given
        String movieName = "some name";
        int year = 2016;
        BigDecimal price = BigDecimal.ONE;

        // when
        Movie persistMovie = movieService.persistMovieInDB(movieName, year, price);
        Movie movieFoundByName = movieService.findMovieByName(movieName);

        // then
        assertThat(movieFoundByName).isNotNull();
        assertThat(movieFoundByName).usingRecursiveComparison().ignoringFields("price").isEqualTo(persistMovie);
    }

    @Nested
    class PriceTests {

        @Autowired
        private MovieService movieService;

        @ParameterizedTest
        @MethodSource
        @DisplayName("Prices between 0.01 and 99.99 should be supported")
        void checkPriceAfterPersisting(BigDecimal inputPrice, BigDecimal expectedPersistedPrice) {
            var movieName = "some movie with price " + expectedPersistedPrice;
            movieService.persistMovieInDB(movieName, 2016, inputPrice);

            var movieInDb = movieService.findMovieByName(movieName);
            assertThat(movieInDb.getPrice()).isEqualTo(expectedPersistedPrice);
        }

        static Stream<Arguments> checkPriceAfterPersisting() {
            return Stream.of(arguments(BigDecimal.valueOf(0.01), BigDecimal.valueOf(0.01)), // minimum price
                    arguments(BigDecimal.valueOf(0.001), BigDecimal.valueOf(0, 2)), // price too small
                    arguments(BigDecimal.valueOf(99.99), BigDecimal.valueOf(99.99))); // maximum price
        }

        @Test
        @DisplayName("Prices equal or greater than 100.00 are not supported")
        void priceTooLargeForDB() {
            assertThatThrownBy(() -> movieService.persistMovieInDB("some movie", 2016, BigDecimal.valueOf(100)))
                    .isInstanceOf(DataIntegrityViolationException.class).hasMessageContaining("A field with precision");
        }
    }

    @Test
    void should_get_all_movies_in_a_year() {
        // given
        String movieName1 = "first movie of 2018";
        String movieName2 = "second movie of 2018";
        movieService.persistMovieInDB(movieName1, 2018, BigDecimal.ONE);
        movieService.persistMovieInDB(movieName2, 2018, BigDecimal.ONE);
        movieService.persistMovieInDB("movie of 2017", 2017, BigDecimal.ONE);

        // when
        Set<Movie> moviesOf2018 = movieService.findMoviesByYear(2018);

        // then
        assertThat(moviesOf2018).hasSize(2);
        assertThat(moviesOf2018).extracting(Movie::getName).containsExactlyInAnyOrder(movieName1, movieName2);
    }

    @Test
    void should_get_all_movies_between_five_and_ten_dollars() {
        // given
        String movieName1 = "movie for 6$";
        String movieName2 = "movie for 8$";
        movieService.persistMovieInDB(movieName1, 2016, BigDecimal.valueOf(6));
        movieService.persistMovieInDB(movieName2, 2016, BigDecimal.valueOf(8));
        movieService.persistMovieInDB("too cheap", 2016, BigDecimal.ONE);
        movieService.persistMovieInDB("too expensive", 2016, BigDecimal.valueOf(20));

        // when
        Set<Movie> moviesOf2018 = movieService.findMoviesInPriceRange(BigDecimal.valueOf(5), BigDecimal.TEN);

        // then
        assertThat(moviesOf2018).hasSize(2);
        assertThat(moviesOf2018).extracting(Movie::getName).containsExactlyInAnyOrder(movieName1, movieName2);
    }
}
