package com.example.ormworkshop.solution1repository.service;

import java.math.BigDecimal;
import java.util.Set;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.example.ormworkshop.solution1repository.datamodel.Movie;
import com.example.ormworkshop.solution1repository.repository.MovieRepository;

@Component
public class MovieService {

    private MovieRepository movieRepository;

    @Autowired
    public MovieService(MovieRepository movieRepository) {
        this.movieRepository = movieRepository;
    }

    public Movie persistMovieInDB(String movieName, Integer year, BigDecimal price) {
        Movie movie = Movie.builder()
                .name(movieName)
                .year(year)
                .price(price)
                .build();

        return movieRepository.save(movie);
    }

    public long countMovies() {
        return movieRepository.count();
    }

    public Movie findMovieById(Long id) {
        return movieRepository.findOneById(id);
    }

    public Movie findMovieByName(String movieName) {
        return movieRepository.findOneByName(movieName);
    }

    public Set<Movie> findMoviesByYear(Integer year) {
        return movieRepository.findAllByYear(year);
    }

    public Set<Movie> findMoviesInPriceRange(BigDecimal minPrice, BigDecimal maxPrice) {
        return movieRepository.findAllByPriceBetween(minPrice, maxPrice);
    }
}
