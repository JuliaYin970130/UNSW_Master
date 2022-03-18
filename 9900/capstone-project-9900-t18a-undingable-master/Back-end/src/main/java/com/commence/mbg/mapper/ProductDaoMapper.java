package com.commence.mbg.mapper;

import com.commence.mbg.model.Product;
import org.apache.ibatis.annotations.Param;

import java.util.List;

/**
 * @program: capstone-project-9900-t18a-undingable
 * @description:
 * @author: Jiahui Wang
 * @create: 2021-10-27 21:28
 **/
public interface ProductDaoMapper {
    List <Product> findAll();

    List <Product> findProductByPriceRange(@Param("low_price") Integer low_price, @Param("high_price") Integer high_price);

}
