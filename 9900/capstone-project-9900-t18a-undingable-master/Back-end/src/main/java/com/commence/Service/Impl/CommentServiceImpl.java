package com.commence.Service.Impl;

import com.commence.Service.CommentService;
import com.commence.Utils.ReturnResult;
import com.commence.mbg.mapper.OrderdetailMapper;
import com.commence.mbg.mapper.OrdersMapper;
import com.commence.mbg.mapper.UserMapper;
import com.commence.mbg.model.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

/**
 * @Program: capstone-project-9900-t18a-undingable
 * @Description:
 * @Date: 2021/11/7 16:55
 * @Auther: Jiahui Wang
 */
@Service
public class CommentServiceImpl implements CommentService {

    @Autowired
    private OrderdetailMapper orderdetailMapper;

    @Autowired
    private OrdersMapper ordersMapper;

    @Autowired
    private UserMapper userMapper;

    @Override
    public ReturnResult viewByProduct_id(Long product_id) {
        if (product_id == null){
            return ReturnResult.failed(503, null, "Please input product ID");
        }
        OrderdetailExample orderdetailExample = new OrderdetailExample();
        orderdetailExample.createCriteria().andProductidEqualTo(product_id);
        List<Orderdetail> orderdetails = orderdetailMapper.selectByExample(orderdetailExample);
        List<CommentReturnobj> commentReturnobjs = new ArrayList<>();
        if (orderdetails.size() > 0){
            for(Orderdetail orderdetail: orderdetails){
                CommentReturnobj commentReturnobj = new CommentReturnobj();
                commentReturnobj.setComment(orderdetail.getComment());
                commentReturnobj.setProductId(orderdetail.getProductid());
                commentReturnobj.setOrder_Id(orderdetail.getOrderid());
                commentReturnobj.setStars(orderdetail.getStars());
                long user_id = ordersMapper.selectByPrimaryKey(commentReturnobj.getOrder_Id()).getUserid();
                User user = userMapper.selectByPrimaryKey(user_id);
                user.setPassword("shadowed");
                commentReturnobj.setUser(user);
                commentReturnobjs.add(commentReturnobj);
            }
        }
        return ReturnResult.success(commentReturnobjs, "return comment via product id successfully");
    }

    @Override
    public ReturnResult viewByOrder_id(Long order_id) {
        if (order_id == null){
            return ReturnResult.failed(503, null, "Please input order ID");
        }
        OrderdetailExample orderdetailExample = new OrderdetailExample();
        orderdetailExample.createCriteria().andOrderidEqualTo(order_id);
        List<Orderdetail> orderdetails = orderdetailMapper.selectByExample(orderdetailExample);
        List<CommentReturnobj> commentReturnobjs = new ArrayList<>();
        if (orderdetails.size() == 0){
            return ReturnResult.failed(503, null, "Please input correct order ID");
        }
        for(Orderdetail orderdetail: orderdetails){
            CommentReturnobj commentReturnobj = new CommentReturnobj();
            commentReturnobj.setComment(orderdetail.getComment());
            commentReturnobj.setProductId(orderdetail.getProductid());
            commentReturnobj.setOrder_Id(orderdetail.getOrderid());
            commentReturnobj.setStars(orderdetail.getStars());
            long user_id = ordersMapper.selectByPrimaryKey(commentReturnobj.getOrder_Id()).getUserid();
            User user = userMapper.selectByPrimaryKey(user_id);
            user.setPassword("shadowed");
            commentReturnobj.setUser(user);
            commentReturnobjs.add(commentReturnobj);
        }
        return ReturnResult.success(commentReturnobjs, "return comment via order id successfully");
    }

    @Override
    public ReturnResult addOrUpdateComment(Long order_id, Long product_id, String comment, int stars) {
        if (order_id == null){
            return ReturnResult.failed(503, null, "Please input order ID");
        }
        if (product_id == null){
            return ReturnResult.failed(503, null, "Please input product ID");
        }
        if (comment == null){
            return ReturnResult.failed(503, null, "Please input comment");
        }
        OrderdetailExample orderdetailExample = new OrderdetailExample();
        orderdetailExample.createCriteria().andOrderidEqualTo(order_id).andProductidEqualTo(product_id);
        System.out.println(orderdetailMapper.selectByExample(orderdetailExample));
        Orderdetail orderdetail = orderdetailMapper.selectByExample(orderdetailExample).get(0);
        orderdetail.setComment(comment);
        orderdetail.setStars(stars);
        int res = orderdetailMapper.updateByPrimaryKey(orderdetail);
        if (res == 1){
            return ReturnResult.success(null, "add or update comment successfully");
        }
        return ReturnResult.failed(504, null, "add or update comment FAILED");
    }
}
