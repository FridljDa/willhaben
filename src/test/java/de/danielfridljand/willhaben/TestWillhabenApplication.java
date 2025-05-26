package de.danielfridljand.willhaben;

import org.springframework.boot.SpringApplication;

public class TestWillhabenApplication {

    public static void main(String[] args) {

        SpringApplication.from(WillhabenApplication::main).with(TestcontainersConfiguration.class).run(args);
    }

}
