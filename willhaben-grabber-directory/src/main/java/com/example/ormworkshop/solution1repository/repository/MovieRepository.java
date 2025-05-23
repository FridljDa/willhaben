package com.example.ormworkshop.solution1repository.repository;

import java.math.BigDecimal;
import java.util.Set;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.example.ormworkshop.solution1repository.datamodel.Movie;

@Repository
public interface MovieRepository extends JpaRepository<Movie, Long> {
    Movie findOneByName(String movieName);

    Movie findOneById(Long id);

    Set<Movie> findAllByYear(Integer year);

    Set<Movie> findAllByPriceBetween(BigDecimal minPrice, BigDecimal maxPrice);
}
