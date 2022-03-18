export const safeParseJSON = (val) => {
	try {
		return JSON.parse(val);
	} catch(e) {
		return null;
	}
};

export const getUserInfo = () => safeParseJSON(window.localStorage.getItem("loginState"));

export const setUserInfo = (user) => {
	delete user.password;
    window.localStorage.setItem("loginState", JSON.stringify(user));
};

export const formatPrice = (originalPrice) => {
	if (!originalPrice) {
		return '??';
	}
	return (originalPrice / 100).toFixed(2);
};