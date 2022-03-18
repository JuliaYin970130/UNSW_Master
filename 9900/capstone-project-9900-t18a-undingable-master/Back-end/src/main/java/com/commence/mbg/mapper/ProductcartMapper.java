package com.commence.mbg.mapper;

import com.commence.mbg.model.Productcart;
import com.commence.mbg.model.ProductcartExample;
import java.util.List;
import org.apache.ibatis.annotations.Param;

public interface ProductcartMapper {
    int countByExample(ProductcartExample example);

    int deleteByExample(ProductcartExample example);

    int deleteByPrimaryKey(Long id);

    int insert(Productcart record);

    int insertSelective(Productcart record);

    List<Productcart> selectByExample(ProductcartExample example);

    Productcart selectByPrimaryKey(Long id);

    int updateByExampleSelective(@Param("record") Productcart record, @Param("example") ProductcartExample example);

    int updateByExample(@Param("record") Productcart record, @Param("example") ProductcartExample example);

    int updateByPrimaryKeySelective(Productcart record);

    int updateByPrimaryKey(Productcart record);
}