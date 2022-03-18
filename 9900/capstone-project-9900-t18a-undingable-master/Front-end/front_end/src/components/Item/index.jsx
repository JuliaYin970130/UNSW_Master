import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import './index.css';

export default class Item extends Component {
    render() {
        const { itemData } = this.props;
        return (
            <Link to={`/itemInfo?id=${itemData.id}`}>
                {/* single product info */}
              <div className="item-card">
                <img src={itemData.imgUrl} alt="Aventus Creed for men" />
                <div className="item-info-block">
                    <p className="item-name">{itemData.name}</p>
                    <p className="brand">{itemData.brand}</p>
                    <p className="sale">{itemData.saleNum.toLocaleString('en-US')} sold</p>
                    <p className="stock">Stock: {itemData.stock}</p>
                </div>
              </div>
            </Link>
        )
    }
}
