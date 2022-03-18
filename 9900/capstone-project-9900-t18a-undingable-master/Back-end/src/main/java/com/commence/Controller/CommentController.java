package com.commence.Controller;

import com.commence.Service.CommentService;
import com.commence.Utils.ReturnResult;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

/**
 * @Program: capstone-project-9900-t18a-undingable
 * @Description:
 * @Date: 2021/11/7 16:55
 * @Auther: Jiahui Wang
 */
@CrossOrigin(origins = "*")
@Controller
@RequestMapping("/comment")
public class CommentController {

    @Autowired
    private CommentService commentService;

    @RequestMapping(value = "/viewByProduct", method = RequestMethod.GET)
    @ResponseBody
    public ReturnResult viewByProduct_id(Long product_id){
        return commentService.viewByProduct_id(product_id);
    }

    @RequestMapping(value = "/viewByOrder", method = RequestMethod.GET)
    @ResponseBody
    public ReturnResult viewByOrder_id(Long order_id){
        return commentService.viewByOrder_id(order_id);
    }

    @RequestMapping(value = "/addOrUpdate", method = RequestMethod.POST)
    @ResponseBody
    public ReturnResult addOrUpdateComment(Long order_id, Long product_id, String comment, int stars){
        return commentService.addOrUpdateComment(order_id, product_id, comment, stars);
    }



}
