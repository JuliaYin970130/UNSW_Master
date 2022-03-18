package com.commence.Service.Impl;

import com.commence.Service.OrderService;
import com.commence.Utils.ReturnResult;
import com.commence.mbg.mapper.OrderdetailMapper;
import com.commence.mbg.mapper.OrdersMapper;
import com.commence.mbg.mapper.ProductcartMapper;
import com.commence.mbg.mapper.ShoppingcartMapper;
import com.commence.mbg.model.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Date;
import java.util.HashSet;
import java.util.List;

/**
 * @Program: capstone-project-9900-t18a-undingable
 * @Description:
 * @Date: 2021/11/7 15:17
 * @Auther: Jiahui Wang
 */
@Service
public class OrderServiceImpl implements OrderService {

    @Autowired
    private OrdersMapper ordersMapper;

    @Autowired
    private OrderdetailMapper orderdetailMapper;

    @Autowired
    private ProductcartMapper productcartMapper;

    @Autowired
    private ShoppingcartMapper shoppingcartMapper;

    /**
     * View Order details via product id
     * @param order_id order id
     * @return
     */
    @Override
    public ReturnResult viewByProductId(Long product_id) {
        if (product_id == null){
            return ReturnResult.failed(400, null, "plase don't input null product id");
        }
        OrderdetailExample orderdetailExample = new OrderdetailExample();
        orderdetailExample.createCriteria().andProductidEqualTo(product_id);
        List<Orderdetail> orderDetails = orderdetailMapper.selectByExample(orderdetailExample);
        HashSet<Long> orderIdList = new HashSet<Long>();
        for ( Orderdetail orderDetail : orderDetails){
            orderIdList.add(orderDetail.getOrderid());
        }
        OrdersExample orderExample = new OrdersExample();
        orderExample.createCriteria().andOrderidIn(new ArrayList<Long>(orderIdList));
        List<Orders> orderList = ordersMapper.selectByExample(orderExample);
        List<OrderReturnObj> orderReturnList = new ArrayList<OrderReturnObj>();
        for (Orders order : orderList) {
            OrderReturnObj orderReturnObj = new OrderReturnObj();
            orderReturnObj.setOrderId(order.getOrderid());
            orderReturnObj.setUserId(order.getUserid());
            orderReturnObj.setOrderTime(order.getOrdertime());
            orderReturnObj.setTotalPrice(order.getAmount());
            orderReturnList.add(orderReturnObj);
        }
        return ReturnResult.success(orderReturnList, "return order details successfully");
    }

    /**
     * View Order details via order id
     * @param order_id order id
     * @return
     */
    @Override
    public ReturnResult viewById(Long order_id) {
        if (order_id == null){
            return ReturnResult.failed(400, null, "plase don't input null order id");
        }
        Orders order = ordersMapper.selectByPrimaryKey(order_id);
        OrderReturnObj orderReturnObj = new OrderReturnObj();
        orderReturnObj.setOrderId(order.getOrderid());
        orderReturnObj.setUserId(order.getUserid());
        orderReturnObj.setOrderTime(order.getOrdertime());
        orderReturnObj.setTotalPrice(order.getAmount());
        OrderdetailExample orderdetailExample = new OrderdetailExample();
        orderdetailExample.createCriteria().andOrderidEqualTo(order_id);
        orderReturnObj.setOrderdetail(orderdetailMapper.selectByExample(orderdetailExample));
    
        return ReturnResult.success(orderReturnObj, "return order details successfully");
    }

    /**
     * View Order details via user id
     * @param user_id User id
     * @return
     */
    @Override
    public ReturnResult view(Long user_id) {
        if (user_id == null){
            return ReturnResult.failed(503, null, "plase don't input null user id");
        }
        OrdersExample orderExample = new OrdersExample();
        orderExample.createCriteria().andUseridEqualTo(user_id);
        List<Orders> orders = ordersMapper.selectByExample(orderExample);

        List<OrderReturnObj> orderReturnObjs = new ArrayList<>();
        for (Orders order: orders){
            OrderReturnObj orderReturnObj = new OrderReturnObj();
            orderReturnObj.setOrderId(order.getOrderid());
            orderReturnObj.setUserId(order.getUserid());
            orderReturnObj.setOrderTime(order.getOrdertime());
            orderReturnObj.setTotalPrice(order.getAmount());
            OrderdetailExample orderdetailExample = new OrderdetailExample();
            orderdetailExample.createCriteria().andOrderidEqualTo(order.getOrderid());
            orderReturnObj.setOrderdetail(orderdetailMapper.selectByExample(orderdetailExample));
            orderReturnObjs.add(orderReturnObj);
        }
        return ReturnResult.success(orderReturnObjs, "return order details successfully");
    }

    @Override
    public ReturnResult checkout(OrderInObj order) {
        if (order.getUserId() == null){
            return ReturnResult.failed(503, null, "please input user ID");
        }
        if (order.getProducts() == null){
            return ReturnResult.failed(503, null, "please input products");
        }
        List<ProductInObj> products = order.getProducts();
        Orders new_order = new Orders();
        new_order.setUserid(order.getUserId());
        new_order.setOrdertime(new Date());
        new_order.setAmount(order.getAmount());
        int res = ordersMapper.insert(new_order);
        Long order_id = new_order.getOrderid();
        System.out.println(order_id);
        List<Long> productList = new ArrayList<>();
        if (res == 1){
            for (ProductInObj product: products){
                productList.add(product.getProduct_id());
                Orderdetail orderdetail = new Orderdetail();
                orderdetail.setOrderid(order_id);
                orderdetail.setProductid(product.getProduct_id());
                orderdetail.setPrice(product.getPrice());
                orderdetail.setQuantity(product.getQuantity());
                int res1 = orderdetailMapper.insert(orderdetail);
                if (res1 != 1){
                    return ReturnResult.failed(505, null, "checkout failed!");
                }
            }
        }
        ClearCart(order.getUserId(), productList);
        return ReturnResult.success(null, "checkout successfully");
    }

    private void ClearCart(Long userId, List<Long> products) {
        ShoppingcartExample shoppingcartExample = new ShoppingcartExample();
        shoppingcartExample.createCriteria().andUserIdEqualTo(userId);
        Long cart_id = shoppingcartMapper.selectByExample(shoppingcartExample).get(0).getCartId();

        ProductcartExample productcartExample = new ProductcartExample();
        productcartExample.createCriteria().andCartIdEqualTo(cart_id);
        List<Productcart> productcarts =  productcartMapper.selectByExample(productcartExample);
        for ( Productcart productcart : productcarts){
            if (products.contains(productcart.getProductId())) {
                productcart.setDeletestatus(1);
                productcartMapper.updateByPrimaryKey(productcart);
            }
        }
    }
}
