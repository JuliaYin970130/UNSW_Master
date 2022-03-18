package com.commence;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.SpringApplication;
import org.springframework.context.annotation.Configuration;

import javax.servlet.*;
import javax.servlet.annotation.WebFilter;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

/**
 * @program: capstone-project-9900-t18a-undingable
 * @description: Main Class
 * @author: Jiahui Wang
 * @create: 2021-09-27 10:33
 **/

@SpringBootApplication
@MapperScan("com.commence.mbg.mapper")
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}

