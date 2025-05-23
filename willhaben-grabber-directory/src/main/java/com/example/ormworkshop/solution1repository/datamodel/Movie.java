package com.example.ormworkshop.solution1repository.datamodel;

import java.math.BigDecimal;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "MOVIE")
public class Movie {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(name = "MOVIE_ID", unique = true, nullable = false)
    private Long id;
    @Column(name = "MOVIE_NAME")
    private String name;
    @Column(name = "YEAR")
    private Integer year;
    // Hint: a BigDecimal has both a value and precision!
    @Column(name = "PRICE", precision = 4, scale = 2)
    private BigDecimal price;

    public static class MovieBuilder {
        private Long id;
        private String name;
        private Integer year;
        private BigDecimal price;

        MovieBuilder() {
        }

        public Movie.MovieBuilder id(final Long id) {
            this.id = id;
            return this;
        }

        public Movie.MovieBuilder name(final String name) {
            this.name = name;
            return this;
        }

        public Movie.MovieBuilder year(final Integer year) {
            this.year = year;
            return this;
        }

        public Movie.MovieBuilder price(final BigDecimal price) {
            this.price = price;
            return this;
        }

        public Movie build() {
            return new Movie(this.id, this.name, this.year, this.price);
        }

        @Override
        public String toString() {
            return "Movie.MovieBuilder(id=" + this.id + ", name=" + this.name + ", year=" + this.year + ", price=" + this.price + ")";
        }
    }

    public static Movie.MovieBuilder builder() {
        return new Movie.MovieBuilder();
    }

    public Long getId() {
        return this.id;
    }

    public String getName() {
        return this.name;
    }

    public Integer getYear() {
        return this.year;
    }

    public BigDecimal getPrice() {
        return this.price;
    }

    public void setId(final Long id) {
        this.id = id;
    }

    public void setName(final String name) {
        this.name = name;
    }

    public void setYear(final Integer year) {
        this.year = year;
    }

    public void setPrice(final BigDecimal price) {
        this.price = price;
    }

    @Override
    public boolean equals(final Object o) {
        if (o == this) return true;
        if (!(o instanceof Movie)) return false;
        final Movie other = (Movie) o;
        if (!other.canEqual((Object) this)) return false;
        final Object this$id = this.getId();
        final Object other$id = other.getId();
        if (this$id == null ? other$id != null : !this$id.equals(other$id)) return false;
        final Object this$name = this.getName();
        final Object other$name = other.getName();
        if (this$name == null ? other$name != null : !this$name.equals(other$name)) return false;
        final Object this$year = this.getYear();
        final Object other$year = other.getYear();
        if (this$year == null ? other$year != null : !this$year.equals(other$year)) return false;
        final Object this$price = this.getPrice();
        final Object other$price = other.getPrice();
        if (this$price == null ? other$price != null : !this$price.equals(other$price)) return false;
        return true;
    }

    protected boolean canEqual(final Object other) {
        return other instanceof Movie;
    }

    @Override
    public int hashCode() {
        final int PRIME = 59;
        int result = 1;
        final Object $id = this.getId();
        result = result * PRIME + ($id == null ? 43 : $id.hashCode());
        final Object $name = this.getName();
        result = result * PRIME + ($name == null ? 43 : $name.hashCode());
        final Object $year = this.getYear();
        result = result * PRIME + ($year == null ? 43 : $year.hashCode());
        final Object $price = this.getPrice();
        result = result * PRIME + ($price == null ? 43 : $price.hashCode());
        return result;
    }

    public Movie() {
    }

    private Movie(final Long id, final String name, final Integer year, final BigDecimal price) {
        this.id = id;
        this.name = name;
        this.year = year;
        this.price = price;
    }

    @Override
    public String toString() {
        return "Movie(id=" + this.getId() + ", name=" + this.getName() + ", year=" + this.getYear() + ", price=" + this.getPrice() + ")";
    }
}
