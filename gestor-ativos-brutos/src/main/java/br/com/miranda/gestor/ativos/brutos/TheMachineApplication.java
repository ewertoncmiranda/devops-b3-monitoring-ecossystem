package br.com.miranda.gestor.ativos.brutos;

import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;
import org.springframework.boot.autoconfigure.orm.jpa.HibernateJpaAutoConfiguration;
import org.springframework.boot.autoconfigure.data.redis.RedisAutoConfiguration;

@Slf4j
@SpringBootApplication(exclude = {
		DataSourceAutoConfiguration.class,
		HibernateJpaAutoConfiguration.class,
		RedisAutoConfiguration.class
})
public class TheMachineApplication {

	public static void main(String[] args) {
		log.info("[MAIN] ========================================");
		log.info("[MAIN] Iniciando aplicação: TheMachineApplication");
		log.info("[MAIN] ========================================");

		SpringApplication.run(TheMachineApplication.class, args);

		log.info("[MAIN] ========================================");
		log.info("[MAIN] Aplicação iniciada com sucesso!");
		log.info("[MAIN] ========================================");
	}
}
