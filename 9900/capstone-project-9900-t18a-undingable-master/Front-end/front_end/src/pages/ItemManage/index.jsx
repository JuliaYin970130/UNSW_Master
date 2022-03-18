import React, { useState, useEffect, Fragment } from 'react';
import qs from 'querystring';
import moment from 'moment';
import { useHistory, useLocation } from 'react-router-dom';
import { queryItems } from '../../apis/product';
import { viewCommentByProductId } from '../../apis/comment';
import { Layout, Table, Button,Tooltip, Rate, message } from "antd";

import './index.css'
import { queryOrderByProductId } from '../../apis/order';
import { formatPrice } from '../../utils';


const ItemManage = () => {
    const history = useHistory();
    const location = useLocation();
    const parsedQuery = qs.parse(location.search.replace('?', ''));
    const itemId = parsedQuery && parsedQuery.id;
    const [itemData, setItemData] = useState(null);
    const [itemComments, setItemComments] = useState([]);
    const [itemOrders, setItemOrders] = useState([]);

    useEffect(() => {
        if (itemId) {
            Promise.all([
                queryItems({
                    id: itemId
                }),
                viewCommentByProductId(itemId),
                queryOrderByProductId(itemId)
            ])
            .then(([[res], comments, orders]) => {
                setItemData(res);
                setItemComments(comments);
                setItemOrders(orders);
            })
            .catch((err) => {
                console.error(err);
                message.error(`Query Error: ${err.message}`);
            })
        } else {
            history.push('/admin')
        }
    }, [itemId, history]);

    const handleDeleteComments = (target) => {
        const newList = itemComments.filter((_val, i) => i !== target);
        setItemComments(newList);
    };

    const { Content } = Layout;

    const orderColumns = [
        {
            title: 'Order ID',
            dataIndex: 'orderId',
            key: 'orderId',
        },
        {
            title: 'Order Date',
            dataIndex: 'orderTime',
            key: 'orderTime',
            render: (val) => moment(val).toLocaleString()
        },
        {
            title: 'Total',
            dataIndex: 'totalPrice',
            key: 'totalPrice',
            render: (val) => 'AU$' + formatPrice(val)
        }
    ];


    const commentColumns = [
        {
            title: "orderId",
            dataIndex: "order_Id",
            key: "order_Id",
        },
        {
            title: "Content",
            dataIndex: "comment",
            key: "comment",
            width: 200,
            ellipsis: {
                showTitle: false,
              },
            render: content => (
                <Tooltip placement="topLeft" title={content}>
                  {content}
                </Tooltip>
              ),
        },
        {
            title: "Rate",
            dataIndex: "stars",
            key: "rate",
            width: 150,
            render: (stars) => <Rate value={stars} />
        },
        {
            title: "Action",
            key: "action",
            render: (_v, _a, i) => (
                <Button type="text" onClick={() => handleDeleteComments(i)}>Delete</Button>
            )
        }
    ];


    return (
        <Content style={{ padding: "0 50px", minHeight: '95vh' }}>
            <div className="item-manage-container">
                {/* order */}
                <div className="item-orders">
                    {itemData ? <Fragment>
                        <h2>{itemData.id} {itemData.name}</h2>

                        <div className="item-info">
                            <span><b>Stock: </b> {itemData.stock} </span>
                            <span><b>Sales: </b> {itemData.saleNum.toLocaleString('en-US')}  </span>
                        </div>
                    </Fragment> : null}

                    {/* <Divider orientation="left">In-progress Orders</Divider>
                    <Table
                        // 表头
                        columns={orderColumns}
                        // 数据
                        dataSource={inprogressData}
                        size="middle"
                        pagination={{ pageSize: 10, size: "small" }}
                        // id="admin-table"
                    />

                    <Divider orientation="left">Completed Orders</Divider> */}
                    <Table
                        // 表头
                        columns={orderColumns}
                        // 数据
                        dataSource={itemOrders.map((item) => ({
                            ...item,
                            key: `order-${item.orderId}`
                        }))}
                        size="middle"
                        pagination={{ pageSize: 10, size: "small" }}
                        // id="admin-table"
                    />

                </div>
                {/* comments */}
                <div className="item-comments">
                    <h2>Comments List</h2>
                    <Table
                        // 表头
                        columns={commentColumns}
                        // 数据
                        dataSource={itemComments.map((item) => ({
                            ...item,
                            key: `item-${item.order_Id}`
                        }))}
                        size="middle"
                        pagination={{ pageSize: 10, size: "small" }}
                        // id="admin-table"
                    />
                </div>
            </div>
        </Content>
    )
}

export default ItemManage;
