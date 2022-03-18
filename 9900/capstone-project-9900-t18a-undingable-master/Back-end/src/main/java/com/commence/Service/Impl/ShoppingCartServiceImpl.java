package com.commence.Service.Impl;

import com.commence.Service.ShoppingCartService;
import com.commence.Utils.ReturnResult;
import com.commence.mbg.mapper.ProductMapper;
import com.commence.mbg.mapper.ProductcartMapper;
import com.commence.mbg.mapper.ShoppingcartMapper;
import com.commence.mbg.model.*;
import com.fasterxml.jackson.databind.util.JSONPObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * @Program: capstone-project-9900-t18a-undingable
 * @Description:
 * @Date: 2021/11/6 15:16
 * @Auther: Jiahui Wang
 */
@Service
public class ShoppingCartServiceImpl implements ShoppingCartService {

    @Autowired
    private ShoppingcartMapper shoppingcartMapper;

    @Autowired
    private ProductcartMapper productcartMapper;

    @Autowired
    private ProductMapper productMapper;

    @Override
    public ReturnResult view(User user) {
        if (user.getId() == null){
            return ReturnResult.failed(503, null, "please give user ID");
        } else {
            ShoppingcartExample shoppingcartExample = new ShoppingcartExample();
            shoppingcartExample.createCriteria().andUserIdEqualTo(user.getId());
            List<Shoppingcart> shoppingcarts =  shoppingcartMapper.selectByExample(shoppingcartExample);
            if (shoppingcarts.size() == 0){
                Shoppingcart shoppingcart = new Shoppingcart();
                shoppingcart.setUserId(user.getId());
                shoppingcartMapper.insert(shoppingcart);
                shoppingcarts =  shoppingcartMapper.selectByExample(shoppingcartExample);
            }

            // this user has already have shopping cart
            Long cart_id = shoppingcarts.get(0).getCartId();
            ProductcartExample productcartExample = new ProductcartExample();
            productcartExample.createCriteria().andCartIdEqualTo(cart_id).andDeletestatusEqualTo(0);
            List<Productcart> productcarts = productcartMapper.selectByExample(productcartExample);

            List<ShoppingCartObj> shoppingCartObjs = new ArrayList<>();
            for (Productcart productcart: productcarts){
                ShoppingCartObj shoppingCartObj = new ShoppingCartObj();
                shoppingCartObj.setShoppingCartId(productcart.getCartId());
                shoppingCartObj.setProduct(productMapper.selectByPrimaryKey(productcart.getProductId()));
                shoppingCartObj.setQuantity(productcart.getQuantity());
                shoppingCartObjs.add(shoppingCartObj);
            }
            return ReturnResult.success(shoppingCartObjs, "Get shopping carts successfully");
        }
    }

    @Override
    public ReturnResult add(Long product_id, Long quantity, Long user_id) {
        if (user_id == null){
            return ReturnResult.failed(503, null, "please give user ID");
        } else {
            ShoppingcartExample shoppingcartExample = new ShoppingcartExample();
            shoppingcartExample.createCriteria().andUserIdEqualTo(user_id);
            List<Shoppingcart> shoppingcarts =  shoppingcartMapper.selectByExample(shoppingcartExample);
            if (shoppingcarts.size() == 0){
                Shoppingcart shoppingcart = new Shoppingcart();
                shoppingcart.setUserId(user_id);
                shoppingcartMapper.insert(shoppingcart);
                shoppingcarts =  shoppingcartMapper.selectByExample(shoppingcartExample);
            }

            // this user has already have shopping cart
            Long cart_id = shoppingcarts.get(0).getCartId();
            ProductcartExample productcartExample = new ProductcartExample();
            productcartExample.createCriteria().andCartIdEqualTo(cart_id).andProductIdEqualTo(product_id).andDeletestatusEqualTo(0);
            List<Productcart> productcartList = productcartMapper.selectByExample(productcartExample);
            if (productcartList.size() == 0) {
                Productcart productcart = new Productcart();
                productcart.setProductId(product_id);
                productcart.setQuantity(quantity);
                productcart.setCartId(cart_id);
                productcart.setDeletestatus(0);
                int res = productcartMapper.insert(productcart);
                if (res == 1){
                    return ReturnResult.success(null, "Add product into shopping cart successfully");
                }
            } else {
                Productcart productcart= productcartList.get(0);
                productcart.setQuantity(quantity + productcart.getQuantity());
                int res = productcartMapper.updateByPrimaryKey(productcart);
                if (res == 1){
                    return ReturnResult.success(null, "Update Quantity successfully");
                }
            }
            return ReturnResult.failed(501, null, "Add product into shopping cart FAILED");
        }
    }

    @Override
    public ReturnResult delete(Long product_id, Long user_id) {
        if (product_id == null || user_id == null){
            return ReturnResult.failed(501, null, "please give user ID or product ID");
        } else {
            ShoppingcartExample shoppingcartExample = new ShoppingcartExample();
            shoppingcartExample.createCriteria().andUserIdEqualTo(user_id);
            List<Shoppingcart> shoppingcarts =  shoppingcartMapper.selectByExample(shoppingcartExample);
            if (shoppingcarts.size() == 0){
                return ReturnResult.failed(502, null, "This user don't have shopping cart");
            } else {
                Long cart_id = shoppingcarts.get(0).getCartId();
                ProductcartExample productcartExample = new ProductcartExample();
                productcartExample.createCriteria().andCartIdEqualTo(cart_id).andProductIdEqualTo(product_id);
                List<Productcart> productcartList = productcartMapper.selectByExample(productcartExample);
                if (productcartList.size() == 0) {
                    return ReturnResult.failed(503, null, "please input correct product_id-- This product is not in shopping cart");
                } else {
                    Productcart productcart= productcartList.get(0);
                    productcart.setDeletestatus(1);
                    int res = productcartMapper.updateByPrimaryKey(productcart);
                    if (res == 1){
                        return ReturnResult.success(null, "Delete product into shopping cart successfully");
                    }
                }

            }
        }
        return ReturnResult.failed(504, null, "Delete product into shopping cart FAILED");
    }

    @Override
    public ReturnResult updateQuantity(Long product_id, Long quantity, Long user_id) {
        if (user_id == null){
            return ReturnResult.failed(503, null, "please give user ID");
        } else {
            ShoppingcartExample shoppingcartExample = new ShoppingcartExample();
            shoppingcartExample.createCriteria().andUserIdEqualTo(user_id);
            List<Shoppingcart> shoppingcarts =  shoppingcartMapper.selectByExample(shoppingcartExample);
            if (shoppingcarts.size() == 0){
                return ReturnResult.failed(502, null, "This user don't have shopping cart");
            }

            // this user has already have shopping cart
            Long cart_id = shoppingcarts.get(0).getCartId();
            ProductcartExample productcartExample = new ProductcartExample();
            productcartExample.createCriteria().andCartIdEqualTo(cart_id).andProductIdEqualTo(product_id);
            List<Productcart> productcartList = productcartMapper.selectByExample(productcartExample);
            if (productcartList.size() == 0) {
                return ReturnResult.failed(503, null, "please input correct product_id-- This product is not in shopping cart");
            } else {
                Productcart productcart= productcartList.get(0);
                if (productcart.getDeletestatus() == 1){
                    return ReturnResult.failed(504, null, "This product has already been deleted!");
                }
                productcart.setQuantity(quantity);
                int res = productcartMapper.updateByPrimaryKey(productcart);
                if (res == 1){
                    return ReturnResult.success(null, "Update Quantity successfully");
                }
            }
        }
        return ReturnResult.failed(504, null, "Update Quantity FAILED");
    }
}
