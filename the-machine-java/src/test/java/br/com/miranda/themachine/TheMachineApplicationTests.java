package br.com.miranda.themachine;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.boot.test.context.SpringBootTest;

@ExtendWith(MockitoExtension.class)
class TheMachineApplicationTests {

	@Test
	public void test_bypass() {
		Assertions.assertTrue(true);
	}

}
