import axios from 'axios';

export const handleReturnResult = (res) => {
    const response = res.data;
    if (response && response.code === 200) {
        return response.data;
    }
    throw new Error(`[${response ? response.code : '-1'}]${response ? response.message : 'Unknown biz server error'}`);
};

export const request = axios.create({
    baseURL: '',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
});