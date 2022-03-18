import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { Link, useHistory } from 'react-router-dom';
import { Card, Image, Checkbox, Button, InputNumber, message } from 'antd';

import { deleteShoppingCart, updateQuantity, viewShoppingCart } from '../../apis/shoppingCart';
import { formatPrice, getUserInfo } from '../../utils';

import './index.css';

const Cart = () => {
    const history = useHistory();
    const [cartItems, setCartItems] = useState([]);

    const fetchItems = useCallback(() => {
        const userInfo = getUserInfo();
        if (!userInfo) {
            history.push('/login');
            return;
        }
        return viewShoppingCart(userInfo.id)
        .then((cartItems) => {
            setCartItems(cartItems.map((item) => ({
                ...item,
                checked: true
            })));
        })
        .catch((err) => {
            message.error(err.message);
        });

    }, [history]);

    const handleQuantityChange = (productId, quantity) => {
        const userInfo = getUserInfo();
        if (!userInfo) {
            history.push('/login');
            return;
        }
        const promise = (quantity === 0) ? deleteShoppingCart(userInfo.id, productId) : updateQuantity(userInfo.id, productId, quantity);
        promise.then(() => {
            fetchItems();
        })
        .catch((err) => {
            message.error(err.message)
        });
    };

    const handleCheckout = () => {
        history.push(`/checkout?itemList=${
            encodeURIComponent(
                JSON.stringify(
                    cartItems.map(
                        (cartItem) => (cartItem.checked ? {
                            id: cartItem.product.id,
                            name: cartItem.product.name,
                            price: cartItem.product.price,
                            quantity: cartItem.quantity
                        } : null)
                    ).filter(v => v)
                )
            )
        }`);
    };

    const totalPrice = useMemo(() => {
        return cartItems.reduce((sum, cartItem) => {
            return sum + (cartItem.product.price * (cartItem.quantity || 1));
        }, 0);
    }, [cartItems]);

    useEffect(() => {
        fetchItems();
    }, [fetchItems]);

    return (
        <div id="cart-page">
            <Card id="cart-box">
                <h1 id="head">Cart</h1>
                {cartItems.length ? <div id="cart-box-body">
                    {cartItems.map((cartItem, i) => <div className="checkout-1">
                        <div className="item-1">
                            <Checkbox checked={cartItem.checked} onChange={(e) => {
                                const { checked } = e.target;
                                const newCartItems = [
                                    ...cartItems
                                ];
                                newCartItems[i].checked = checked;
                                setCartItems(newCartItems);
                            }}>
                                <Image
                                    width={80}
                                    src={cartItem.product.imgUrl}
                                />
                            </Checkbox>
                        </div>
                        <Link className="item-2" to={`/itemInfo?id=${cartItem.product.id}`}>
                            <span className="itemName">{cartItem.product.name}</span>
                            <span>Size: {cartItem.product.size}ml</span>
                        </Link>
                        <div className="item-3">
                            <span className="price">
                                <small>AU$</small>{formatPrice(cartItem.product.price)}
                            </span>
                            <span style={{ margin: 10 }}> x </span>
                            <InputNumber min={0} value={cartItem.quantity} onChange={(val) => handleQuantityChange(cartItem.product.id, val)} />
                        </div>
                    </div>)}
                    <div className="checkout-2">
                        <div></div>
                        <div></div>
                        <h1>Total:</h1>
                        <div className="total-price"><small>AU$</small>{formatPrice(totalPrice)}</div>
                    </div>
                    <div className="checkout-3">
                        <div></div>
                        <div>
                            <Link to="/" className="skip">
                                <Button id="skip-btn">Back</Button>
                            </Link>
                        </div>
                        <div></div>
                        <div>
                            <Button
                                id="checkout-button"
                                type="primary"
                                onClick={() => handleCheckout()}
                            >
                                Check out
                            </Button>
                        </div>

                    </div>
                </div> : 
                <div id="cart-box-body-empty">
                    <span className="cart-empty-text">
                            There is no items.
                    </span>
                    <Link to="/" className="skip">
                        <Button id="skip-btn">Back to Home</Button>
                    </Link>
                </div>}
            </Card>
        </div>
    )
};


export default Cart;