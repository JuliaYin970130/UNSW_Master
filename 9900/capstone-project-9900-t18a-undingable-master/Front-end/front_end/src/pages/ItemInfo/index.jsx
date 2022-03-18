import React, { useState, useEffect } from 'react';
import { useLocation, useHistory } from 'react-router-dom';
import qs from 'querystring';
import moment from 'moment';
import { Layout, Breadcrumb, Image, InputNumber, Button, Rate, Card, Comment, Tooltip, List, Spin, message } from 'antd';
import { queryItems } from '../../apis/product';
import { viewCommentByProductId } from '../../apis/comment';
import { addShoppingCart } from '../../apis/shoppingCart';
import { formatPrice, getUserInfo } from '../../utils';

import './index.css';

const { Content } = Layout;

const ItemInfo = () => {
    const history = useHistory();
    const location = useLocation();
    const parsedQuery = qs.parse(location.search.replace('?', ''));
    const itemId = parsedQuery && parsedQuery.id;
    const [itemData, setItemData] = useState(null);
    const [itemComments, setItemComments] = useState([]);
    const [quantity, setQuantity] = useState(1);

    const handleAddCart = () => {
        const userInfo = getUserInfo();
        if (!userInfo) {
            history.push('/login');
            return;
        }
        addShoppingCart(userInfo.id, itemId, quantity)
        .then(() => {
            setQuantity(1);
            history.push('/cart');
        })
        .catch((err) => {
            message.error(err.message);
        });
    };

    const handleCheckOut = () => {
        history.push(`/checkout?itemList=${encodeURIComponent(JSON.stringify([{
            id: itemData.id,
            name: itemData.name,
            price: itemData.price,
            quantity
        }]))}`);
    };

    useEffect(() => {
        if (itemId) {
            Promise.all([
                queryItems({
                    id: itemId
                }),
                viewCommentByProductId(itemId)
            ])
            .then(([[res], comments]) => {
                setItemData(res);
                setItemComments(comments);
            })
            .catch((err) => {
                console.error(err);
                message.error(`Query Error: ${err.message}`);
            })
        }
    }, [itemId]);

    if (!itemId) {
        return <Content style={{ marginTop: "64px", padding: '0 50px', minHeight: "100vh" }}>
            <h1>Error: no itemId by router</h1>
        </Content>;
    }

    if (!itemData) {
        return <Content style={{ marginTop: "64px", padding: '0 50px', minHeight: "100vh", display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Spin />
        </Content>;
    }

    // average star
    const starArr = itemComments.map((commentItem) => (commentItem.stars)).filter(v => v);
    const starSum = starArr.reduce((sum, curVal) => sum+curVal, 0);
    const starAvg = starSum / starArr.length;

    // comment content
    const data = itemComments.map((commentItem) => (commentItem && commentItem.comment && commentItem.stars ? {
        author: commentItem.user.name,
        avatar: 'https://joeschmoe.io/api/v1/random',
        content: (
            <p>{commentItem.comment}</p>
        ),
        datetime: (
            <Tooltip title={moment().subtract(1, 'days').format('YYYY-MM-DD HH:mm:ss')}>
                <span>{moment().subtract(1, 'days').fromNow()}</span>
            </Tooltip>
        )
    } : null)).filter(v => v);

    return (
        <Content style={{ padding: '0 50px', minHeight: "100vh" }}>
            {/* 标签位置 */}
            <Breadcrumb style={{ margin: '16px 0' }}>
                <Breadcrumb.Item>Home</Breadcrumb.Item>
                <Breadcrumb.Item>Products</Breadcrumb.Item>
                <Breadcrumb.Item>item</Breadcrumb.Item>
            </Breadcrumb>

            <div className="item-contanier">
                {/* A part - img + basicinfo + price */}
                <div className="top-container">
                    {/* Image */}
                    <div className="item-img">
                        <Image
                            width={250}
                            src={itemData.imgUrl}
                        />
                    </div>

                    {/* basicinfo */}
                    <div className="basicinfo">
                        <p className="item-name">{itemData.name}</p>
                        <h3>Brand: {itemData.brand} </h3>
                        <p>Size: {itemData.size}ml </p>

                        {/* star */}
                        <Rate disabled value={starAvg} /> 
                        {/* sales */}
                        <span className="sales"> ({itemData.saleNum.toLocaleString('en-US')} sold) </span>

                        <div className="price">
                            AU${formatPrice(itemData.price)}
                        </div>

                        {/* number */}
                        <div className="quantity">
                            <span>Quantity: </span>
                            <InputNumber min={1} max={1000} value={quantity} onChange={(val) => setQuantity(val)} />
                            {
                                quantity <= itemData.stock
                                ? <span style={{margin:"10px 10px", color:'#90be6d'}}> (Available in Stock!) </span>
                                : <span style={{margin:"10px 10px", color:'#FF5000'}}> (Out Stock!) </span>
                            }
                        </div>

                        <Button type="primary" style={{ margin: '10px 10px 10px 0' }} onClick={() => handleAddCart()}>Add to Cart</Button>
                        <Button type="primary" onClick={() => handleCheckOut()}>Buy Now</Button>

                    </div>

                </div>


                {/* B part - description + comments*/}

                <div className="bottom-container">
                    {/* descroption*/}
                    <div className="description">

                        <Card title="Description" bordered={false} className="card" style={{ fontSize: "15px" }}>
                            <p><b>Scent Note:</b> {itemData.scentNotes}</p>
                            <p><b>Grender:</b> {itemData.gender}</p>
                            <p>{itemData.description}</p>
                        </Card>

                    </div>

                    {/* comment */}
                    <div className="comments">
                        <List
                            className="comment-list"
                            header={`${data.length} replies`}
                            itemLayout="horizontal"
                            dataSource={data}
                            renderItem={item => (
                                <li>
                                    <Comment
                                        actions={item.actions}
                                        author={item.author}
                                        avatar={item.avatar}
                                        content={item.content}
                                        datetime={item.datetime}
                                    />
                                </li>
                            )}
                        />
                    </div>
                </div>
            </div>
        </Content>
    )
};

export default ItemInfo;
