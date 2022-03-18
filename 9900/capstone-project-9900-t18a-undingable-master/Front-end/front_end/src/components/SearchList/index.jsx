import React, { useState, useEffect } from 'react';
import { Space, Card, Form, Input, Button, message, Pagination, Spin } from 'antd';

import Item from '../Item';
import { queryItems } from '../../apis/product';
import { safeParseJSON } from "../../utils";

import './index.css';

const SearchList = ({
  keyword
}) => {
  const [min, setMin] = useState(0);
  const [max, setMax] = useState(10);
  const [isLoading, setIsLoading] = useState(true);
  const [searchResult, setSearchResult] = useState([]);

  const userInfo = safeParseJSON(window.localStorage.getItem("loginState"));

  useEffect(() => {
    if (!keyword) {
      return;
    }

    setIsLoading(true);
    return queryItems({
      name: keyword
    }).then((res) => {
      setSearchResult(res);
      setIsLoading(false);
    })
      .catch((err) => {
        console.error(err);
        message.error((err && err.message) || 'Unknown error');
        setIsLoading(false);
      });
  }, [keyword])

  const handleChange = (value) => {
    if (value <= 1) {
      setMin(0);
      setMax(10);
    } else {
      setMin((value - 1) * 10);
      setMax((value - 1) * 10 + 10);
    }
  };

  const onFinish = (values) => {
    console.log("Success:", values);
    message.success("Thanks for request!");
  };

  const onFinishFailed = (errorInfo) => {
    console.log("Failed:", errorInfo);
  };

  if (isLoading) {
    return (
      <div className="search-item">
        <Space size="large" wrap>
          <Spin />
        </Space>
      </div>
    );
  }

  // search result
  if (Array.isArray(searchResult) && searchResult.length !== 0) {
    return (
      <div className="search-item">
        <Space size="large" wrap>
          {searchResult.slice(min, max).map((itemData) => <Item itemData={itemData} key={'SearchList-' + itemData.id} />)}
        </Space>
        <Pagination
          defaultCurrent={1}
          defaultPageSize={10}
          onChange={handleChange}
          total={searchResult.length}
          style={{ textAlign: "center", marginTop: 10, marginLeft: "-80px" }}
        />
      </div>
    );
  } else {
    if (userInfo) {
      // no search result
      return (
        <div className="empty">
          <h2>We don’t have anything that matches your query </h2>
          <h3>
            Check your spelling and try again or use a more general search term.
          </h3>
          <h3>
            Or, send a<a href="/#"> request form </a>
            to us.
          </h3>
          {/* request form */}
          <Card
            title="Request Form"
            style={{ width: 500, margin: "40px 500px 40px auto" }}
          >
            <Form
              name="basic"
              labelCol={{ span: 6 }}
              wrapperCol={{ span: 12 }}
              initialValues={{ remember: true }}
              onFinish={onFinish}
              onFinishFailed={onFinishFailed}
              autoComplete="off"
            >
              <Form.Item
                label="Item name"
                name="Item"
                rules={[
                  { required: true, message: "Please input a item name!" },
                ]}
              >
                <Input />
              </Form.Item>
              <Form.Item
                label="Brand name"
                name="brand"
                rules={[{ required: true, message: "Please input a brand!" }]}
              >
                <Input />
              </Form.Item>

              <Form.Item wrapperCol={{ offset: 6, span: 16 }}>
                <Button type="primary" htmlType="submit">
                  Submit
                </Button>
              </Form.Item>
            </Form>
          </Card>
        </div>
      );

    }else{
      return(
        <div className="empty">
          <h2>We don’t have anything that matches your query </h2>
          <h3>
            Check your spelling and try again or use a more general search term.
          </h3>
        </div>
      )
    }
  }
};

export default SearchList;
