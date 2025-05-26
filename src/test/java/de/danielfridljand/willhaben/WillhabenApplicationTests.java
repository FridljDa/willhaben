package de.danielfridljand.willhaben;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.annotation.Import;

@Import(TestcontainersConfiguration.class)
@SpringBootTest
class WillhabenApplicationTests {

    @Test
    void contextLoads() {

    }

}
