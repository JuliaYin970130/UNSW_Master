package com.commence.mbg.model;

import java.util.ArrayList;
import java.util.List;

public class QuestionaireExample {
    protected String orderByClause;

    protected boolean distinct;

    protected List<Criteria> oredCriteria;

    public QuestionaireExample() {
        oredCriteria = new ArrayList<Criteria>();
    }

    public void setOrderByClause(String orderByClause) {
        this.orderByClause = orderByClause;
    }

    public String getOrderByClause() {
        return orderByClause;
    }

    public void setDistinct(boolean distinct) {
        this.distinct = distinct;
    }

    public boolean isDistinct() {
        return distinct;
    }

    public List<Criteria> getOredCriteria() {
        return oredCriteria;
    }

    public void or(Criteria criteria) {
        oredCriteria.add(criteria);
    }

    public Criteria or() {
        Criteria criteria = createCriteriaInternal();
        oredCriteria.add(criteria);
        return criteria;
    }

    public Criteria createCriteria() {
        Criteria criteria = createCriteriaInternal();
        if (oredCriteria.size() == 0) {
            oredCriteria.add(criteria);
        }
        return criteria;
    }

    protected Criteria createCriteriaInternal() {
        Criteria criteria = new Criteria();
        return criteria;
    }

    public void clear() {
        oredCriteria.clear();
        orderByClause = null;
        distinct = false;
    }

    protected abstract static class GeneratedCriteria {
        protected List<Criterion> criteria;

        protected GeneratedCriteria() {
            super();
            criteria = new ArrayList<Criterion>();
        }

        public boolean isValid() {
            return criteria.size() > 0;
        }

        public List<Criterion> getAllCriteria() {
            return criteria;
        }

        public List<Criterion> getCriteria() {
            return criteria;
        }

        protected void addCriterion(String condition) {
            if (condition == null) {
                throw new RuntimeException("Value for condition cannot be null");
            }
            criteria.add(new Criterion(condition));
        }

        protected void addCriterion(String condition, Object value, String property) {
            if (value == null) {
                throw new RuntimeException("Value for " + property + " cannot be null");
            }
            criteria.add(new Criterion(condition, value));
        }

        protected void addCriterion(String condition, Object value1, Object value2, String property) {
            if (value1 == null || value2 == null) {
                throw new RuntimeException("Between values for " + property + " cannot be null");
            }
            criteria.add(new Criterion(condition, value1, value2));
        }

        public Criteria andQuestionireidIsNull() {
            addCriterion("questionireId is null");
            return (Criteria) this;
        }

        public Criteria andQuestionireidIsNotNull() {
            addCriterion("questionireId is not null");
            return (Criteria) this;
        }

        public Criteria andQuestionireidEqualTo(Long value) {
            addCriterion("questionireId =", value, "questionireid");
            return (Criteria) this;
        }

        public Criteria andQuestionireidNotEqualTo(Long value) {
            addCriterion("questionireId <>", value, "questionireid");
            return (Criteria) this;
        }

        public Criteria andQuestionireidGreaterThan(Long value) {
            addCriterion("questionireId >", value, "questionireid");
            return (Criteria) this;
        }

        public Criteria andQuestionireidGreaterThanOrEqualTo(Long value) {
            addCriterion("questionireId >=", value, "questionireid");
            return (Criteria) this;
        }

        public Criteria andQuestionireidLessThan(Long value) {
            addCriterion("questionireId <", value, "questionireid");
            return (Criteria) this;
        }

        public Criteria andQuestionireidLessThanOrEqualTo(Long value) {
            addCriterion("questionireId <=", value, "questionireid");
            return (Criteria) this;
        }

        public Criteria andQuestionireidIn(List<Long> values) {
            addCriterion("questionireId in", values, "questionireid");
            return (Criteria) this;
        }

        public Criteria andQuestionireidNotIn(List<Long> values) {
            addCriterion("questionireId not in", values, "questionireid");
            return (Criteria) this;
        }

        public Criteria andQuestionireidBetween(Long value1, Long value2) {
            addCriterion("questionireId between", value1, value2, "questionireid");
            return (Criteria) this;
        }

        public Criteria andQuestionireidNotBetween(Long value1, Long value2) {
            addCriterion("questionireId not between", value1, value2, "questionireid");
            return (Criteria) this;
        }

        public Criteria andUseridIsNull() {
            addCriterion("userId is null");
            return (Criteria) this;
        }

        public Criteria andUseridIsNotNull() {
            addCriterion("userId is not null");
            return (Criteria) this;
        }

        public Criteria andUseridEqualTo(Long value) {
            addCriterion("userId =", value, "userid");
            return (Criteria) this;
        }

        public Criteria andUseridNotEqualTo(Long value) {
            addCriterion("userId <>", value, "userid");
            return (Criteria) this;
        }

        public Criteria andUseridGreaterThan(Long value) {
            addCriterion("userId >", value, "userid");
            return (Criteria) this;
        }

        public Criteria andUseridGreaterThanOrEqualTo(Long value) {
            addCriterion("userId >=", value, "userid");
            return (Criteria) this;
        }

        public Criteria andUseridLessThan(Long value) {
            addCriterion("userId <", value, "userid");
            return (Criteria) this;
        }

        public Criteria andUseridLessThanOrEqualTo(Long value) {
            addCriterion("userId <=", value, "userid");
            return (Criteria) this;
        }

        public Criteria andUseridIn(List<Long> values) {
            addCriterion("userId in", values, "userid");
            return (Criteria) this;
        }

        public Criteria andUseridNotIn(List<Long> values) {
            addCriterion("userId not in", values, "userid");
            return (Criteria) this;
        }

        public Criteria andUseridBetween(Long value1, Long value2) {
            addCriterion("userId between", value1, value2, "userid");
            return (Criteria) this;
        }

        public Criteria andUseridNotBetween(Long value1, Long value2) {
            addCriterion("userId not between", value1, value2, "userid");
            return (Criteria) this;
        }

        public Criteria andFamilyIsNull() {
            addCriterion("family is null");
            return (Criteria) this;
        }

        public Criteria andFamilyIsNotNull() {
            addCriterion("family is not null");
            return (Criteria) this;
        }

        public Criteria andFamilyEqualTo(String value) {
            addCriterion("family =", value, "family");
            return (Criteria) this;
        }

        public Criteria andFamilyNotEqualTo(String value) {
            addCriterion("family <>", value, "family");
            return (Criteria) this;
        }

        public Criteria andFamilyGreaterThan(String value) {
            addCriterion("family >", value, "family");
            return (Criteria) this;
        }

        public Criteria andFamilyGreaterThanOrEqualTo(String value) {
            addCriterion("family >=", value, "family");
            return (Criteria) this;
        }

        public Criteria andFamilyLessThan(String value) {
            addCriterion("family <", value, "family");
            return (Criteria) this;
        }

        public Criteria andFamilyLessThanOrEqualTo(String value) {
            addCriterion("family <=", value, "family");
            return (Criteria) this;
        }

        public Criteria andFamilyLike(String value) {
            addCriterion("family like", value, "family");
            return (Criteria) this;
        }

        public Criteria andFamilyNotLike(String value) {
            addCriterion("family not like", value, "family");
            return (Criteria) this;
        }

        public Criteria andFamilyIn(List<String> values) {
            addCriterion("family in", values, "family");
            return (Criteria) this;
        }

        public Criteria andFamilyNotIn(List<String> values) {
            addCriterion("family not in", values, "family");
            return (Criteria) this;
        }

        public Criteria andFamilyBetween(String value1, String value2) {
            addCriterion("family between", value1, value2, "family");
            return (Criteria) this;
        }

        public Criteria andFamilyNotBetween(String value1, String value2) {
            addCriterion("family not between", value1, value2, "family");
            return (Criteria) this;
        }

        public Criteria andForwhoIsNull() {
            addCriterion("forWho is null");
            return (Criteria) this;
        }

        public Criteria andForwhoIsNotNull() {
            addCriterion("forWho is not null");
            return (Criteria) this;
        }

        public Criteria andForwhoEqualTo(String value) {
            addCriterion("forWho =", value, "forwho");
            return (Criteria) this;
        }

        public Criteria andForwhoNotEqualTo(String value) {
            addCriterion("forWho <>", value, "forwho");
            return (Criteria) this;
        }

        public Criteria andForwhoGreaterThan(String value) {
            addCriterion("forWho >", value, "forwho");
            return (Criteria) this;
        }

        public Criteria andForwhoGreaterThanOrEqualTo(String value) {
            addCriterion("forWho >=", value, "forwho");
            return (Criteria) this;
        }

        public Criteria andForwhoLessThan(String value) {
            addCriterion("forWho <", value, "forwho");
            return (Criteria) this;
        }

        public Criteria andForwhoLessThanOrEqualTo(String value) {
            addCriterion("forWho <=", value, "forwho");
            return (Criteria) this;
        }

        public Criteria andForwhoLike(String value) {
            addCriterion("forWho like", value, "forwho");
            return (Criteria) this;
        }

        public Criteria andForwhoNotLike(String value) {
            addCriterion("forWho not like", value, "forwho");
            return (Criteria) this;
        }

        public Criteria andForwhoIn(List<String> values) {
            addCriterion("forWho in", values, "forwho");
            return (Criteria) this;
        }

        public Criteria andForwhoNotIn(List<String> values) {
            addCriterion("forWho not in", values, "forwho");
            return (Criteria) this;
        }

        public Criteria andForwhoBetween(String value1, String value2) {
            addCriterion("forWho between", value1, value2, "forwho");
            return (Criteria) this;
        }

        public Criteria andForwhoNotBetween(String value1, String value2) {
            addCriterion("forWho not between", value1, value2, "forwho");
            return (Criteria) this;
        }

        public Criteria andLowerpriceIsNull() {
            addCriterion("lowerPrice is null");
            return (Criteria) this;
        }

        public Criteria andLowerpriceIsNotNull() {
            addCriterion("lowerPrice is not null");
            return (Criteria) this;
        }

        public Criteria andLowerpriceEqualTo(Long value) {
            addCriterion("lowerPrice =", value, "lowerprice");
            return (Criteria) this;
        }

        public Criteria andLowerpriceNotEqualTo(Long value) {
            addCriterion("lowerPrice <>", value, "lowerprice");
            return (Criteria) this;
        }

        public Criteria andLowerpriceGreaterThan(Long value) {
            addCriterion("lowerPrice >", value, "lowerprice");
            return (Criteria) this;
        }

        public Criteria andLowerpriceGreaterThanOrEqualTo(Long value) {
            addCriterion("lowerPrice >=", value, "lowerprice");
            return (Criteria) this;
        }

        public Criteria andLowerpriceLessThan(Long value) {
            addCriterion("lowerPrice <", value, "lowerprice");
            return (Criteria) this;
        }

        public Criteria andLowerpriceLessThanOrEqualTo(Long value) {
            addCriterion("lowerPrice <=", value, "lowerprice");
            return (Criteria) this;
        }

        public Criteria andLowerpriceIn(List<Long> values) {
            addCriterion("lowerPrice in", values, "lowerprice");
            return (Criteria) this;
        }

        public Criteria andLowerpriceNotIn(List<Long> values) {
            addCriterion("lowerPrice not in", values, "lowerprice");
            return (Criteria) this;
        }

        public Criteria andLowerpriceBetween(Long value1, Long value2) {
            addCriterion("lowerPrice between", value1, value2, "lowerprice");
            return (Criteria) this;
        }

        public Criteria andLowerpriceNotBetween(Long value1, Long value2) {
            addCriterion("lowerPrice not between", value1, value2, "lowerprice");
            return (Criteria) this;
        }

        public Criteria andHigherpriceIsNull() {
            addCriterion("HigherPrice is null");
            return (Criteria) this;
        }

        public Criteria andHigherpriceIsNotNull() {
            addCriterion("HigherPrice is not null");
            return (Criteria) this;
        }

        public Criteria andHigherpriceEqualTo(Long value) {
            addCriterion("HigherPrice =", value, "higherprice");
            return (Criteria) this;
        }

        public Criteria andHigherpriceNotEqualTo(Long value) {
            addCriterion("HigherPrice <>", value, "higherprice");
            return (Criteria) this;
        }

        public Criteria andHigherpriceGreaterThan(Long value) {
            addCriterion("HigherPrice >", value, "higherprice");
            return (Criteria) this;
        }

        public Criteria andHigherpriceGreaterThanOrEqualTo(Long value) {
            addCriterion("HigherPrice >=", value, "higherprice");
            return (Criteria) this;
        }

        public Criteria andHigherpriceLessThan(Long value) {
            addCriterion("HigherPrice <", value, "higherprice");
            return (Criteria) this;
        }

        public Criteria andHigherpriceLessThanOrEqualTo(Long value) {
            addCriterion("HigherPrice <=", value, "higherprice");
            return (Criteria) this;
        }

        public Criteria andHigherpriceIn(List<Long> values) {
            addCriterion("HigherPrice in", values, "higherprice");
            return (Criteria) this;
        }

        public Criteria andHigherpriceNotIn(List<Long> values) {
            addCriterion("HigherPrice not in", values, "higherprice");
            return (Criteria) this;
        }

        public Criteria andHigherpriceBetween(Long value1, Long value2) {
            addCriterion("HigherPrice between", value1, value2, "higherprice");
            return (Criteria) this;
        }

        public Criteria andHigherpriceNotBetween(Long value1, Long value2) {
            addCriterion("HigherPrice not between", value1, value2, "higherprice");
            return (Criteria) this;
        }

        public Criteria andBrandIsNull() {
            addCriterion("brand is null");
            return (Criteria) this;
        }

        public Criteria andBrandIsNotNull() {
            addCriterion("brand is not null");
            return (Criteria) this;
        }

        public Criteria andBrandEqualTo(String value) {
            addCriterion("brand =", value, "brand");
            return (Criteria) this;
        }

        public Criteria andBrandNotEqualTo(String value) {
            addCriterion("brand <>", value, "brand");
            return (Criteria) this;
        }

        public Criteria andBrandGreaterThan(String value) {
            addCriterion("brand >", value, "brand");
            return (Criteria) this;
        }

        public Criteria andBrandGreaterThanOrEqualTo(String value) {
            addCriterion("brand >=", value, "brand");
            return (Criteria) this;
        }

        public Criteria andBrandLessThan(String value) {
            addCriterion("brand <", value, "brand");
            return (Criteria) this;
        }

        public Criteria andBrandLessThanOrEqualTo(String value) {
            addCriterion("brand <=", value, "brand");
            return (Criteria) this;
        }

        public Criteria andBrandLike(String value) {
            addCriterion("brand like", value, "brand");
            return (Criteria) this;
        }

        public Criteria andBrandNotLike(String value) {
            addCriterion("brand not like", value, "brand");
            return (Criteria) this;
        }

        public Criteria andBrandIn(List<String> values) {
            addCriterion("brand in", values, "brand");
            return (Criteria) this;
        }

        public Criteria andBrandNotIn(List<String> values) {
            addCriterion("brand not in", values, "brand");
            return (Criteria) this;
        }

        public Criteria andBrandBetween(String value1, String value2) {
            addCriterion("brand between", value1, value2, "brand");
            return (Criteria) this;
        }

        public Criteria andBrandNotBetween(String value1, String value2) {
            addCriterion("brand not between", value1, value2, "brand");
            return (Criteria) this;
        }
    }

    public static class Criteria extends GeneratedCriteria {

        protected Criteria() {
            super();
        }
    }

    public static class Criterion {
        private String condition;

        private Object value;

        private Object secondValue;

        private boolean noValue;

        private boolean singleValue;

        private boolean betweenValue;

        private boolean listValue;

        private String typeHandler;

        public String getCondition() {
            return condition;
        }

        public Object getValue() {
            return value;
        }

        public Object getSecondValue() {
            return secondValue;
        }

        public boolean isNoValue() {
            return noValue;
        }

        public boolean isSingleValue() {
            return singleValue;
        }

        public boolean isBetweenValue() {
            return betweenValue;
        }

        public boolean isListValue() {
            return listValue;
        }

        public String getTypeHandler() {
            return typeHandler;
        }

        protected Criterion(String condition) {
            super();
            this.condition = condition;
            this.typeHandler = null;
            this.noValue = true;
        }

        protected Criterion(String condition, Object value, String typeHandler) {
            super();
            this.condition = condition;
            this.value = value;
            this.typeHandler = typeHandler;
            if (value instanceof List<?>) {
                this.listValue = true;
            } else {
                this.singleValue = true;
            }
        }

        protected Criterion(String condition, Object value) {
            this(condition, value, null);
        }

        protected Criterion(String condition, Object value, Object secondValue, String typeHandler) {
            super();
            this.condition = condition;
            this.value = value;
            this.secondValue = secondValue;
            this.typeHandler = typeHandler;
            this.betweenValue = true;
        }

        protected Criterion(String condition, Object value, Object secondValue) {
            this(condition, value, secondValue, null);
        }
    }
}