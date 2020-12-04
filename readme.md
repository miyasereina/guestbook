# 留言板任务接口

## 全局错误码

`401`:未登录

### 错误返回格式

```
{
	"status": 401
	"message": "请先登录"，
	"data": null
}
```

## 查看留言

```
/borad
```

### Response Body

```
{
	"nickname": string
	"content": string
	"post_time":timestamp
	"last_correct":timestamp
}
```

## 注册接口

```
POST /user
```

请求参数

```
{
	"username": string
	"password": string
}
```

响应参数

**成功时：**

```
{
	"status": 200
	"msg": "注册成功"
}
```

**失败时：**

`HTTP/1.1 400 Bad Request`

```
1. 缺少参数 username

2. 缺少参数 nickname

3. 缺少参数 password
   缺少参数 sex

4. username参数已存在
```

## 登录接口

```
POST /session
```

**请求参数**

```
{
	"username": string
	"password": string
}
```

**响应参数**

```
{
	"status": 200
	"msg": "登陆成功"
	“data”: {"username":"password"}
}
```

## 发表留言

```
POST /guestbook
```

## 修改留言

```
POST /guestbook/content
```

## 删除留言

```
POST /guestbook/deletion
```

