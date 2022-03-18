package com.commence.Utils;

/**
 * @program: Back-end
 * @description: Common result return type
 * @author: Jiahui Wang
 * @create: 2021-10-09 16:46
 **/
public class ReturnResult<T> {

    /**
     * status code
     */
    private long code;

    /**
     * message
     */
    private String message;

    /**
     * Data
     */
    private T data;

    /**
     * if success, then return
     */
    public static <T> ReturnResult<T> success(T data, String message) {
        return new ReturnResult<T>(200, message, data);
    }

    /**
     * if failed, then return
     */
    public static <T> ReturnResult<T> failed(int code, T data, String message) {
        return new ReturnResult<T>(code, message, data);
    }

    public ReturnResult(long code, String message, T data) {
        this.code = code;
        this.message = message;
        this.data = data;
    }

    public ReturnResult(long code, String message) {
        this.code = code;
        this.message = message;
    }

    public long getCode() {
        return code;
    }

    public void setCode(long code) {
        this.code = code;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public T getData() {
        return data;
    }

    public void setData(T data) {
        this.data = data;
    }

    @Override
    public String toString() {
        return "ReturnResult{" +
                "code=" + code +
                ", message='" + message + '\'' +
                ", data=" + data +
                '}';
    }
}
