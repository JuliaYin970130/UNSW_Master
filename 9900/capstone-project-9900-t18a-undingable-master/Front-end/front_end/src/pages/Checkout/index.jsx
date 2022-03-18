import React, { useMemo, useEffect, Fragment } from 'react';
import { Link, useLocation, useHistory } from 'react-router-dom';
import { Layout, Card, Form, Input, Button, Divider, Collapse, message } from 'antd';
import qs from 'querystring';
import { formatPrice, getUserInfo, safeParseJSON } from '../../utils';

import './index.css';
import { checkout } from '../../apis/order';

const { Content } = Layout;
const Checkout = () => {
    const userInfo = getUserInfo();
    const location = useLocation();
    const history = useHistory();
    const productList = useMemo(() => {
        const { itemList } = qs.parse(location.search.replace('?', ''));
        return safeParseJSON(itemList);
    }, [location]);

    const totalPrice = useMemo(() => {
        return productList.reduce((sum, productItem) => {
            return sum + (productItem.price * productItem.quantity);
        }, 0);
    }, [productList]);


    useEffect(() => {
        if (!userInfo) {
            history.push('/login');
        }
    }, [userInfo, history]);

    useEffect(() => {
        if (!Array.isArray(productList) || !productList.length) {
            message.error('Bad request');
            history.push('/');
        }
    }, [productList, history]);

    const { Panel } = Collapse;

    const onSaveShipInfo = (values) => {
        console.log('Success:', values);
    };

    const onCheckOut = (values) => {
        console.log('Success:', values);
        checkout(userInfo.id, productList.reduce((map, productItem, i) => {
            map[`products[${i}].product_id`] = productItem.id;
            map[`products[${i}].price`] = productItem.price;
            map[`products[${i}].quantity`] = productItem.quantity;
            return map;
        }, {}), totalPrice)
        .then((res) => {
            console.log('checkout', res);
            history.push('/eval');
        })
        .catch((err) => {
            message.error(err.message);
        });
    };


    return (
        <Content style={{ padding: '0 50px', minHeight: "95vh" }}>
            
            <h1 id="title">Check Out</h1>

            <div className="checkout-container">
                {/* shipping info */}
                <div className="shipping">
                    <Card title="Ship to" bordered={false}>
                        <p>Please fill in your shipping information</p>
                        <Form
                            name="shipping"
                            wrapperCol={{ span: 20 }}
                            onFinish={onSaveShipInfo}
                            autoComplete="off"
                            initialValues={userInfo}
                        >
                            <Form.Item
                                name="name"
                                required
                                rules={[{ required: true, message: 'Please input your full name!' }]}
                            >
                                <Input placeholder="Full name" />
                            </Form.Item>

                            <Form.Item
                                name="phone"
                                required
                                rules={[{ required: true, message: 'Please input your Phone!' }]}
                            >
                                <Input placeholder="Phone"/>
                            </Form.Item>
                            <Form.Item
                                name="email"
                                required
                                rules={[{ required: true, message: 'Please input your Email!' }]}
                            >
                                <Input placeholder="Email" />
                            </Form.Item>
                            <Form.Item
                                name="address"
                                required
                                rules={[{ required: true, message: 'Please input your Address!' }]}
                            >
                                <Input placeholder="Address" />
                            </Form.Item>
                        </Form>
                    </Card>

                    {/* checkout */}
                    <Card title="Pay with" bordered={false}>
                        <Collapse defaultActiveKey={['1']}>
                            <Panel showArrow={false} header="Debit or credit card" key="1">
                                {/* <p>{text}</p> */}
                                <Form
                                    name="debit-card"
                                    wrapperCol={{ offset: 1, span: 20 }}
                                    onFinish={onCheckOut}
                                    autoComplete="off"
                                >
                                    <Form.Item
                                        rules={[{ required: true, message: 'Please input your full name!' }]}
                                    >
                                        <Input placeholder="Card Holder name" />
                                    </Form.Item>

                                    <Form.Item
                                        rules={[{ required: true, message: 'Please input your Phone!' }]}
                                    >
                                        <Input placeholder="Card number" />
                                    </Form.Item>
                                    <Form.Item
                                        rules={[{ required: true, message: 'Please input your Email!' }]}
                                    >
                                        <Input placeholder="Expriy MM/YYYY" style={{ width: "46%", marginRight: 10 }} />
                                        <Input placeholder="Security code" style={{ width: "51%" }} />
                                    </Form.Item>
                                </Form>
                                <Button type="primary" block style={{ marginTop: 20 }} onClick={onCheckOut} >
                                    Place Order
                                </Button>
                            </Panel>
                            <Panel showArrow={false} header="PayPal" key="2">
                                <Link to="/eval">
                                    <Button type="primary" htmlType="submit" block style={{ marginTop: 20 }} >
                                        Place Order
                                    </Button>
                                </Link>

                            </Panel>
                            {/* <Checkbox onChange={onChange}>PayPal</Checkbox> */}
                            {/* <Checkbox onChange={onChange}>Gift card</Checkbox> */}
                        </Collapse>
                        {/* <Checkbox onChange={onChange} defaultChecked style={{ marginBottom: 20 }}>Debit or credit card</Checkbox> */}
                    </Card>
                </div>
                {/* Order Summay */}
                <div className="Order">
                    <Card title="Order Summay" bordered={false}>
                        <div className="order-summary">
                            {productList.map((productItem) => (
                                <div className="order-summary-item">
                                    <span className="order-info">Item name: <Link to={`/itemInfo?id=${productItem.id}`}>{productItem.name}</Link></span>
                                    <span className="order-info">Quantity: {productItem.quantity}</span>
                                    <span className="order-info">Price: AU${formatPrice(productItem.price)}</span>
                                    <Divider />
                                </div>
                            ))}
                            <p style={{color:"#ff0a54"}}>Total: AU${formatPrice(totalPrice)}</p>
                        </div>
                        <Link to='/cart'>
                            <Button block>
                                Back to Cart
                            </Button>
                        </Link>
                    </Card>
                </div>
            </div>
        </Content>
    )
}
export default Checkout;
