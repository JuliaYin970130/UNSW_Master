package com.commence.Service;

import com.commence.Utils.ReturnResult;

/**
 * @Program: capstone-project-9900-t18a-undingable
 * @Description:
 * @Date: 2021/11/7 16:55
 * @Auther: Jiahui Wang
 */
public interface CommentService {
    ReturnResult viewByProduct_id(Long product_id);

    ReturnResult viewByOrder_id(Long order_id);

    ReturnResult addOrUpdateComment(Long order_id, Long product_id, String comment, int stars);
}
