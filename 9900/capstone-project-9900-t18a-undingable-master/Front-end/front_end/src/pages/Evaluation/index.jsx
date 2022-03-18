import React, { useEffect, useState } from 'react';
// import ReactDOM from 'react-dom';
import { Link, useHistory, useLocation } from 'react-router-dom';
import { Button, Layout, Space, Image, Rate, Input, Card, message } from 'antd';
import qs from 'querystring';
import { HeartFilled } from '@ant-design/icons';
import { queryItems } from '../../apis/product';
import { queryOrderById } from '../../apis/order';

import './index.css';
import { addOrUpdateComment } from '../../apis/comment';

const {Content} = Layout;
const {TextArea} = Input;

const Evaluation = () => {
    const history = useHistory();
    const location = useLocation();
    const parsedQuery = qs.parse(location.search.replace('?', ''));
    const orderId = parsedQuery && parsedQuery.orderId;

    const [commentList, setCommentList] = useState(null);

    const handleChangeField = (i, key, val) => {
        const newList = [
            ...commentList
        ];
        newList[i][key] = val;
        setCommentList(newList);
    };

    const handleSubmitComment = () => {
        for (const commentItem of commentList) {
            if (!commentItem.stars || !commentItem.comment) {
                continue;
            }
            addOrUpdateComment(orderId, commentItem.productid, commentItem.stars, commentItem.comment)
            .then(() => {
                message.success('Success!');
                history.push('/user');
            })
            .catch((err) => {
                message.error(err.message);
            });
        }
    };

    useEffect(() => {
        if (!orderId) {
            history.push('/');
            return;
        }
        queryOrderById(orderId)
        .then((res) => {
            console.log(res);
            if (!res || !Array.isArray(res.orderdetail)) {
                throw new Error('Invalid response');
            }
            return Promise.all(
                res.orderdetail.map(
                    (commentItem) => queryItems({
                        id: commentItem.productid
                    }).then(([productItem]) => ({
                        ...commentItem,
                        name: productItem.name,
                        imgUrl: productItem.imgUrl
                    }))
                )
            );
        })
        .then((commentList) => setCommentList(commentList))
        .catch((err) => {
            message.error(err.message);
        });
    }, [orderId, history]);

    return (
        <Content style={{ padding: '0 50px', minHeight: "720px" }}>
            
            <h1 id="title">How's your shopping experience?</h1>
            <div className="eval-box">
                <Card title="Evaluation" bordered={false}>
                    <div className="eval-area">
                        {Array.isArray(commentList) ? commentList.map((productItem, i) => <div key={`comment-${productItem.id}`}>
                            <Image
                                width={80}
                                src={productItem.imgUrl}
                            />
                            <div className="eval-info-block">
                                <span>{productItem.name} x {productItem.quantity}</span>
                                <Rate character={ <HeartFilled /> } value={productItem.stars} onChange={(val) => handleChangeField(i, 'stars', val)} />
                            </div>
                            <TextArea placeholder="Comment" value={productItem.comment} onChange={(e) => handleChangeField(i, 'comment', e.target.value)} style={{ marginLeft: 10 }} />
                        </div>) : null}
                    </div>
                </Card>
                <div className="bot-area">
                    <Space size={40}>
                        <Button type="primary" onClick={handleSubmitComment}>Submit</Button>
                        <Link to="/">
                            <Button>Not this time</Button>
                        </Link>
                    </Space>
                </div>
            </div>
        </Content>

    )
};

export default Evaluation;
