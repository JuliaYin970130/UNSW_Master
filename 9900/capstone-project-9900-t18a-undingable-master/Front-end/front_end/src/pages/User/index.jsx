import React, { useState, useEffect, useMemo } from "react";
import { Layout, Form, Input, Button, Select, Divider, Table, message } from "antd";
import { Link } from 'react-router-dom';
import { queryOrderList } from "../../apis/order";
import { formatPrice, getUserInfo, setUserInfo } from "../../utils";


import "./index.css";
import { updateProfile } from "../../apis/user";

const parsePhone = (val = '') => {
    const regResult = /(\+\d{2})\d+/.exec(val);
    const prefix = (regResult && regResult[1]) || '';
    return [prefix, val ? val.replace(prefix, '') : ''];
};

const User = () => {
    const [phonePrefix, setPhonePrefix] = useState('');
    const [phone, setPhone] = useState('');
    const [orderList, setOrderList] = useState([]);

    const userInfo = useMemo(() => getUserInfo(), []);

    useEffect(() => {
        queryOrderList(userInfo.id)
            .then((res) => {
                setOrderList(res);
            })
            .catch((err) => {
                message.error(err.message);
            });
        const [phonePrefix, phone] = parsePhone(userInfo.phone);
        setPhonePrefix(phonePrefix);
        setPhone(phone);
    }, [userInfo]);

    const handleUpdateProfile = (values) => {
        const newUserInfo = {
            ...userInfo,
            ...values,
            phone: phonePrefix + phone
        };
        updateProfile(newUserInfo)
            .then((res) => {
                setUserInfo(newUserInfo);
                message.success('Success!');
            })
            .catch((err) => {
                message.error(err.message);
            });
    };

    const { Content } = Layout;
    const { Option } = Select;
    // form type
    const layout = {
        labelCol: {
            span: 7,
        },
        wrapperCol: {
            span: 16,
        },
    };

    // validate Messages
    /* eslint-disable no-template-curly-in-string */

    const validateMessages = {
        required: "${label} is required!",
        types: {
            email: "${label} is not a valid email!",
            number: "${label} is not a valid number!",
        },
    };
    /* eslint-enable no-template-curly-in-string */

    // mobile country number
    const prefixSelector = (
        <Form.Item noStyle>
            <Select value={phonePrefix} onChange={(val) => setPhonePrefix(val)} style={{ width: 100 }}>
                <Option value="+61">
                    <div className="prefixFlag">
                        <img
                            src="https://flagcdn.com/16x12/au.png"
                            srcSet="https://flagcdn.com/32x24/au.png 2x,https://flagcdn.com/48x36/au.png 3x"
                            width="16"
                            height="12"
                            alt="Austrlia" />
                        <span>+61</span>
                    </div>
                </Option>
                <Option value="+86">
                    <div className="prefixFlag">
                        <img
                            src="https://flagcdn.com/16x12/cn.png"
                            srcSet="https://flagcdn.com/32x24/cn.png 2x,https://flagcdn.com/48x36/cn.png 3x"
                            width="16"
                            height="12"
                            alt="China" />
                        <span>+86</span>
                    </div>
                </Option>
            </Select>
        </Form.Item>
    );

    // form title
    const columns = [
        { title: 'Order ID', dataIndex: 'orderId', key: 'orderId' },
        { title: 'Order Date', dataIndex: 'orderTime', key: 'orderTime' },
        { title: 'Total', dataIndex: 'totalPrice', key: 'totalPrice' },
        { title: 'Action', dataIndex: 'orderId', key: 'action', render: (id) => <Link to={`/eval?orderId=${id}`}>Evaluate</Link> },
    ];

    return (
        <Content
            className="user-container"
            style={{ padding: "0 50px", marginTop: 64, minHeight: 700 }}
        >
            {/* user info update */}
            <div className="user-profile">
                <h2>Profile</h2>
                <Divider orientation="left">Profile Update</Divider>
                <Form
                    {...layout}
                    className="user-form"
                    name="nest-messages"
                    validateMessages={validateMessages}
                    initialValues={userInfo}
                    onFinish={handleUpdateProfile}
                >
                    {/* User name */}
                    <Form.Item
                        name="name"
                        label="User Name"
                        rules={[
                            {
                                required: true,
                            },
                        ]}
                    >
                        <Input />
                    </Form.Item>
                    {/* Email */}
                    <Form.Item
                        name="email"
                        label="Email"
                        rules={[
                            {
                                type: 'email',
                                message: 'The input is not valid E-mail!',
                            },
                            {
                                required: true,
                                message: 'Please input your E-mail!',
                            },
                        ]}
                    >
                        <Input />
                    </Form.Item>

                    {/* mobile num */}
                    <Form.Item
                        label="Phone Number"
                        rules={[{ required: true, message: 'Please input your phone number!' }]}
                    >
                        <Input
                            addonBefore={prefixSelector}
                            value={phone}
                            onChange={(e) => {
                                const { value: val } = e.target;
                                setPhone(val);
                            }}
                            style={{ width: '100%' }} />
                    </Form.Item>

                    {/* address */}
                    <Form.Item
                        name='address'
                        label="Address"
                        rules={[
                            {
                                required: true,
                                message: 'Please input your Address!'
                            },
                        ]}
                    >
                        <Input />
                    </Form.Item>

                    {/* submit */}
                    <Form.Item wrapperCol={{ ...layout.wrapperCol, offset: 7 }}>
                        <Button type="primary" htmlType="submit">
                            Update
                        </Button>
                    </Form.Item>
                </Form>

                <Divider orientation="left">Questionnaire</Divider>
                <Link to='/questionaire'>
                    <Button type="primary" htmlType="submit" style={{ marginLeft: 30 }}>
                        Update / Fill in the Questionnaire
                    </Button>
                </Link>


            </div>

            {/* user oder */}
            <div className="user-order">
                <h2>Order List</h2>

                {/* 进展中的订单 */}
                {/* <Divider orientation="left">In-progress Orders</Divider>
                <Table
                    // 表头
                    columns={columns}
                    // 数据
                    dataSource={orderList.map((orderItem) => ({
                        ...orderItem,
                        key: orderItem.orderId,
                        orderTime: new Date(orderItem.orderTime).toLocaleString(),
                        totalPrice: 'AU$' + formatPrice(orderItem.totalPrice)
                    }))}
                    size="middle"
                    pagination={{ pageSize: 3, size: "small" }}
                /> */}


                {/* 完成的订单 */}
                {/* <Divider orientation="left">Completed Orders</Divider> */}

                <Table
                    // 表头
                    columns={columns}
                    // 数据
                    dataSource={orderList.map((orderItem) => ({
                        ...orderItem,
                        key: orderItem.orderId,
                        orderTime: new Date(orderItem.orderTime).toLocaleString(),
                        totalPrice: 'AU$' + formatPrice(orderItem.totalPrice)
                    }))}
                    size="middle"
                    pagination={{ pageSize: 8, size: "small" }}
                />

            </div>

        </Content>
    );
}

export default User;