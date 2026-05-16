package br.com.miranda.gestor.ativos.brutos;

import lombok.extern.slf4j.Slf4j;
import static br.com.miranda.gestor.ativos.brutos.tools.ConstantesUtils.MAIN;
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
public class GestorAtivosBrutosApplication {

	public static void main(String[] args) {
		log.info("{} ========================================", MAIN);
		log.info("{} Iniciando aplicação: GestorAtivosBrutosApplication", MAIN);
		log.info("{} ========================================", MAIN);

		SpringApplication.run(GestorAtivosBrutosApplication.class, args);

		log.info("{} ========================================", MAIN);
		log.info("{} Aplicação iniciada com sucesso!", MAIN);
		log.info("{} ========================================", MAIN);
	}
}
