## 🚧 **[python-web-template]：Python敏捷开发项目模板！** 🚀

兄弟们，江湖救急！是不是还在为每天写CRUD，搞得头昏脑涨？是不是还在为屎山代码，半夜惊醒？别慌，老哥我今天心情好，带你们整个狠活！
别再写屎山了,让我们开始屎上雕花吧.gogogo!

## 敏捷开发和屎山？

国内很多项目都追求敏捷开发，快速上线，但往往就变成了堆屎山。没办法，时间紧任务重嘛。但Python天生适合敏捷开发，语法简单，开发速度快，成本低。
但是！即使是屎山，咱也要尽量让他好看点，毕竟程序员每天都要面对它。接下来分享一些我多年来的经验，让你的项目既能快速上线，又能保持一定的优雅。

### 这玩意儿是啥

这是一个Python敏捷开发项目模板，是我多年码代码的血泪总结，不整那些花里胡哨的，直接上干货！让你快速撸起袖子搞项目，还能保持代码的优雅，不至于将来维护的时候想砍自己。
web框架选了fastapi,支持异步,速度快,配套多,自带pydantic验证,swagger文档,挺好.


### 灵感来源

我承认，确实借鉴了点DDD（领域驱动设计）的思路，但没完全照搬，毕竟Python的优势是啥？快速开发！咱不能搞得太复杂，把人都给整晕了。主要吸取了 Domain（领域）、Service（服务）、Repositories（仓库）、Event（事件）这些概念，目的是让业务逻辑更清晰，代码模块化，方便后期扩展。


### Repository模式

这个模式我可太喜欢了！CRUD操作都封装好了，你直接调用就行，不用关心底层逻辑，就像用遥控器控制电视一样简单。还对一些通用逻辑做了处理，比如 `is_deleted` 这种软删除，你不用每次都写 `where is_deleted=False` ，直接用就行，方便得一批！

### 为啥不直接用DDD?

DDD确实牛逼，但用在小型项目上就有点杀鸡用牛刀了。现在都是ai时代了,用python开发项目的基本上更倾向于敏捷开发，快速上线才是王道。如果你要搞大型项目，那把Domain就按照 `infra/seedwork` 的模式复制到你的子应用就行了，`seedwork` 里放一些全局模块。
当然我也看到一些好的关于python的DDD设计项目 例如https://github.com/pgorecki/python-ddd, 不过这个repo不是基于async的web框架写的

### 有些好用的DDD的精髓借鉴到本项目的

DDD有几个点我是真心觉得好用：

1.  **领域隔离：** 这玩意儿能帮你把业务拆分得明明白白，方便后续扩展。比如，`Domain A` 下面有 `repo A` ，管理 `table A` 的 CRUD，`Domain B` 下面有 `repo B` ，管理 `table B` 的 CRUD。 如果 `A` 服务要更新 `table B` ，那就调用 `Domain B` 对外暴露的接口，而不是直接操作 `repo B` 或者 `table B` 。明白不？

2.  **事件（Event）：** 如果 `Domain A` 涉及到 `Domain B` 的业务，别傻乎乎地把 `Domain B` 引入到 `Domain A` 里，然后组装参数，直接调用 `Domain B`。你应该用事件（Event）去通知 `Domain B`，让它自己去搞定。
    **举个栗子：** 你是开发 `Domain A` 的，你只需要通知 `Domain B`：“嘿，哥们，你该干活了”，至于 `Domain B` 怎么干，跟你没半毛钱关系！这样分工明确，大家都轻松，扯皮的事也少。
    **这里很重要，敲黑板！** 这也是团队协作的关键，责任边界要划分清晰，谁的锅谁背！ 代码也是一样

3.  **核心思想：** 各司其职，职责单一，不要越界！每个人管好自己的一亩三分地，别啥都想掺一脚。 
      有的人我都不稀得说,一个文件写路由,写认证,写参数校验,写查库,好家伙,大锅菜,一勺全烩了. 有的人倒是知道代码分层,什么MVC啥的,就是写着写着就乱了.



### 编程原则

网上一搜一大堆的原则，猛地一看没啥吊用,仔细看看,嗯,有点吊用,顺便贴在下面,随意看看：

```markdown
1. SOLID 原则

    SOLID 原则是面向对象编程和设计中的五个基本原则，由 Robert C. Martin (Uncle Bob) 提出。这些原则可以帮助我们创建更灵活、可维护和易于扩展的代码。
    
    S - Single Responsibility Principle (单一职责原则)
        描述: 一个类或模块应该只有一个引起它变化的原因。换句话说，一个类应该只负责一项职责。
        目的: 提高类的内聚性，减少类的耦合性，使其更易于理解、修改和测试。
    
    O - Open/Closed Principle (开闭原则)
        描述: 软件实体（类、模块、函数等）应该对扩展开放，对修改关闭。也就是说，当需要增加新功能时，应该通过扩展现有代码来实现，而不是修改现有代码。
        目的: 减少代码的修改带来的风险，提高代码的复用性和可维护性。

    L - Liskov Substitution Principle (里氏替换原则)
        描述: 子类型必须能够替换它们的基类型。换句话说，任何使用基类型的地方，都可以使用其子类型，而不会出现错误
        目的: 保证代码的正确性和可扩展性，符合面向对象编程的继承原则。
    
    I - Interface Segregation Principle (接口隔离原则)
        描述: 客户端不应该被迫依赖它们不使用的接口。应该将大的接口拆分为更小的、更具体的接口，客户端只需要依赖它们需要的接口。
        目的: 减少类的耦合性，提高系统的灵活性和可复用性。
    
    D - Dependency Inversion Principle (依赖倒置原则)
        描述:高层模块不应该依赖低层模块，两者都应该依赖抽象。
        抽象不应该依赖细节，细节应该依赖抽象。
        目的: 减少模块之间的耦合性，提高代码的灵活性和可维护性。

2. DRY 原则 (Don't Repeat Yourself - 不要重复自己)
    描述: 避免代码重复。 如果你发现你正在写相同的代码多次，应该考虑将其提取到一个方法或类中，并进行复用
    目的: 提高代码的可维护性和复用性，减少代码的错误。
   
3. YAGNI 原则 (You Aren't Gonna Need It - 你不需要它)
    描述: 不要添加你认为将来可能会需要的特性，除非你现在确实需要它。
    目的: 避免过度设计，减少不必要的复杂性，提高开发效率。
   
4. KISS 原则 (Keep It Simple, Stupid - 保持简单，傻瓜式)
    描述: 保持你的代码简单易懂。 避免不必要的复杂性。
    目的: 提高代码的可读性和可维护性，减少错误的发生。

5. Law of Demeter (迪米特法则) / Least Knowledge Principle (最少知识原则)
    描述: 一个对象应该尽可能少地了解其他对象。 对象应该只与它的直接朋友通信。
    目的: 减少对象之间的耦合性，提高代码的灵活性和可维护性。
   
6. Composition over Inheritance (组合优于继承)
    描述: 尽量使用组合的方式来实现代码复用，而不是使用继承。
    目的: 避免继承带来的耦合性和灵活性问题。

```


<!-- tree -I "__init__*" -->
## 目录结构🌳
... （这里放你的目录结构，用 tree 命令生成）...


### 屎山雕花的建议
虽然都是建屎山,但我们的目标不一样,我们得在屎上雕花,哎,还能在屎上玩花活儿的才是我们真正拉屎人的精神。

项目开始阶段一定一定要
1. 项目开始就定好代码规范，特别是多人开发的时候,毕竟人和人的思维/经历都不一样,一人一个风格真是的难受啊....
2. 项目开始就要接入测试，不然真的就没机会了,铁子!!! 你记住,测试接入就这一次机会，用 pytest/coverage 搞起来啊！


## **此项目到底帮你做了啥？**🎁
下面才是最重要的,让我们稍微正经一点[谁TM写个readme都烧的不行啊]

*   **自动格式化代码：** 每次提交代码都自动格式化，让你的代码整整齐齐，强迫症患者的福音！
*   **数据库迁移：** `alembic` 帮你管理数据库迁移，告别手动修改数据库的烦恼！
*   **依赖管理：** `poetry` 帮你管理依赖，再也不用担心版本冲突了！
*   **日志管理：**  用 loguru 替代标准库的 logging，更好用，更方便,支持异步记录,支持json格式 
*   **环境管理：**  `local`, `dev`, `prod` 三种环境，配置灵活切换，想怎么跑就怎么跑！
*   **数据库操作封装：**  不用重复写 CRUD， 直接调用封装好的方法就行了，爽！
*   **请求模型验证：**  用 `pydantic` 定义 API 请求模型，类型校验不在话下！
*   **统一异常处理：**  API 层和 Service 层的异常处理逻辑都给你安排好了，再也不用为异常发愁了！
*   **请求上下文管理：**  每个请求都有自己的上下文，再也不用担心数据混乱了！
*   **漂亮的代码目录：**  目录结构清晰，让你赏心悦目，维护起来也舒心！


### 我的开发理念
记住我的口号：能不引入第三方库，就TM不引入！自己能搞定的，绝不依赖别人，这才是真男人！所以项目的基础依赖比较简单

### 关于环境变量
其实,fastapi引用的pydantic,默认支持.env的文件的加载. 但我感觉.env的格式报好看,哈哈^.~
所以在不引入第三方库的原则下,我用了from configparser import ConfigParser 去解析xxx.ini的配置文件.对多个环境变量配置文件的管理

### 关于自定义模型
1. API 层基于 pydantic 的自定义 scheme 做为请求 api 的基础模型
2. 也就是说,从api请求进来->到数据库orm模型->到service层操作数据->到api响应出去,你无需手动进行模型转换
3. 基础模型定义在src/infra/seedwork/domain/entities.py,api模型在src/infra/seedwork/api/api_base_scheme.py,定义写好了嗷,其他逻辑你自己加嗷,别懒嗷

### 关于Middleware
1. AccessLogMiddleware会记录所有请求的信息,工作还是要留痕的,并自动转成curl信息,如果真的报错,直接拿着curl信息可以很方便的本地模拟
2. AuthMiddleware认证中间件,先基于jwt实现了一个日常api的auth,然后再对oapi实现了一个api_key的认证, 如果你觉得不够用就自己写吧,铁汁. [对了,这里默认实现了api/oapi的两套路由,分别配了不同的认证auth]
3. GlobalExceptionHandlerMiddleware统一异常处理,包括fastapi的异常和自定义的异常
4. CORSMiddleware 跨域配置，具体的域名啥的,你自己搞呗

### 关于api请求
1. 用contextVar来管理请求上下文,每个请求分配request_id,记录user信息,在请求的生命周期内全局可用
2. api入参的模型都用pydantic进行参数校验啊,别在router/Service写那些基础校验了,哥们儿
3. api的返回值使用统一的数据结构AppResponse,包括code, message, data, request_id. 以及统一的handler,ResponseHandler.success(entity) ResponseHandler.error(entity)
实际的序列化的逻辑交由fastapi的response model来实现即 @router.get("/student/{student_id}", response_model=AppResponse[StudentResp])
虽然不指定response model也行,但是pydantic model毕竟可以加一层校验,还可以过过滤参数.比如有些字段没有在StudentResp声明,entity就算有字段也不会返回给前端,挺好


```text  access_log 记录的curl信息
2025-01-15T14:57:00.239882+0800 - INFO - acess_log.py:42 - dispatch - Request as curl: curl -X GET http://127.0.0.1:8088/api/courses/3/students -H 'connection: keep-alive' -H 'sec-ch-ua-platform: "macOS"' -H 'authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTczNjkyNTI2MX0.73bUzIdIN0ckbWZ6EPsgEZBY2Md4Vv1dg-xINBU22SE' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36' -H 'accept: application/json, text/plain, */*' -H 'sec-ch-ua: "Chromium";v="131", "Not_A Brand";v="24"' -H 'dnt: 1' -H 'sec-ch-ua-mobile: ?0' -H 'sec-fetch-site: same-origin' -H 'sec-fetch-mode: cors' -H 'sec-fetch-dest: empty' -H 'referer: http://127.0.0.1:8088/static/index.html' -H 'accept-encoding: gzip, deflate, br, zstd' -H 'accept-language: zh-CN,zh;q=0.9
```

### 关于日志
用了loguru替代标准库的logging,支持异步记录,支持json格式,其他功能就自己google吧

### 关于数据库有几个优化点
1. 在repository层,在create/update操作之前对pydantic模型->sqlalchemy orm模型的转换
2. 同样的封装好的gets/get_by_id操作之后,查到的对象也是基于BaseEntity[pydantic]的对象,可以直接操作,不会影响orm对象.
3. 实现Service和repo层的数据隔离

还有数据库的几个坑,也说明一下
1. 首先我一直觉得少要用外键约束,级联操作,用起来是简单,很容易出问题. 所以得数据库关联字段得自己维护,你只有显式的写出来才说明你做了某些操作.要不后期定位问题的时候,就得花大时间去查了.
2. 当前第一条是我的个人经验,每个人经验不一样,你可以自己根据自己的经验来选择
3. 这里用的sqlalchemy session是async session. 异步session在对func对象,或者relationship的对象加载时,是lazy load,只有真正取值的时候,才会进行二次查询.所有在转化成BaseEntity对象的时候会有问题,所以复杂查询自己在repo层自己写就行了
4. 



最后说一句

这项目我可是花了心血的，希望你能喜欢。别忘了给个Star！

就到这里，各位老铁，江湖再见！ 😎

## 其实还想在做点啥呢
### todo list
1. just file
2. vercel
