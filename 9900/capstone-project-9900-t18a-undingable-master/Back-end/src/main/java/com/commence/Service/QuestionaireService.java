package com.commence.Service;

import com.commence.Utils.ReturnResult;
import com.commence.mbg.model.Questionaire;

/**
 * @Program: capstone-project-9900-t18a-undingable
 * @Description:
 * @Date: 2021/11/4 16:51
 * @Auther: Jiahui Wang
 */
public interface QuestionaireService {
    ReturnResult get_questionnaire(Questionaire questionaire);

    ReturnResult insert_questionnaire(Questionaire questionaire);

    ReturnResult update_questionnaire(Questionaire questionaire);
}
