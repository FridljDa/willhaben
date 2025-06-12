package de.danielfridljand.willhaben.listing.datamodel;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import java.util.logging.Level;
import java.util.logging.Logger;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table; //TODO org.hibernate.orm instead?

import lombok.Data;
import lombok.NoArgsConstructor;

@Entity //TODO what does this do?
@Table(name = "Listing")
@Data
@NoArgsConstructor
public class Listing {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "ADDITIONAL_COST_DEPOSIT")
    private String additionalCostDeposit;

    @Column(name = "ADDITIONAL_COST_FEE")
    private String additionalCostFee;

    @Column(name = "AVAILABLE_DATE")
    private LocalDateTime availableDate;

    @Column(name = "BUILDING_CONDITION")
    private String buildingCondition;

    @Column(name = "BUILDING_TYPE")
    private String buildingType;

    @Column(name = "Befristung")
    private String befristung;

    @Column(name = "DESCRIPTION", columnDefinition = "TEXT")
    private String description;

    @Column(name = "DURATION_HASTERMLIMIT")
    private Boolean durationHasTermLimit;

    @Column(name = "DURATION_TERMLIMITTEXT")
    private String durationTermLimitText;

    @Column(name = "ESTATE_PREFERENCE")
    private String estatePreference;

    @Column(name = "ESTATE_SIZE")
    private Double estateSize;

    @Column(name = "FLOOR")
    private Integer floor;

    @Column(name = "FLOOR_SURFACE")
    private Double floorSurface;

    @Column(name = "GENERAL_TEXT_ADVERT_Lage", columnDefinition = "TEXT")
    private String generalTextAdvertLage;

    @Column(name = "GENERAL_TEXT_ADVERT_Sonstiges", columnDefinition = "TEXT")
    private String generalTextAdvertSonstiges;

    @Column(name = "HEATING")
    private String heating;

    @Column(name = "LOCATION_ADDRESS_1")
    private String locationAddress1;

    @Column(name = "NO_OF_ROOMS")
    private Double noOfRooms;

    @Column(name = "OWNAGETYPE")
    private String ownageType;

    @Column(name = "PROPERTY_TYPE")
    private String propertyType;

    @Column(name = "RENTAL_PRICE_ADDITIONAL_COST_GROSS")
    private Double rentalPriceAdditionalCostGross;

    @Column(name = "RENTAL_PRICE_PER_MONTH")
    private Double rentalPricePerMonth;

    @Column(name = "RENTAL_PRICE_TOTAL_ENCUMBRANCE")
    private Double rentalPriceTotalEncumbrance;

    @Column(name = "Verfuegbarkeit")
    private String verfuegbarkeit;

    @Column(name = "available_date")
    private LocalDateTime availableDateAlternative;

    @Column(name = "url")
    private String url;
}