## GET `/api/users`

Получение списка юзеров,
в текущей реализации они доступны только для юзеров с ролью "admin"

> должна быть авторизация

```ts
export type RedisFSortRawFilter = {
    gte?: number;
    lte?: number;
    isempty?: boolean;
    any?: string[] | RedisFSortRawFilter[];
    some?: string[];
    exists?: boolean;
    match?: string;
}

export type Pagination<T> = {
    filter?: {
        [key in keyof T]?: string | RedisFSortRawFilter;
    };
    sortBy?: string;
    order?: PaginationOrderType;
    offset?: number;
    limit?: number;
    expiration?: number;
}

export type PaginationResp<T> = {
    items: T[];
    cursor: number;
    page: number;
    pages: number;
    total: number;
}

export type UsersRequest = Pagination<User>;
export type UsersResponse = PaginationResp<User>;
```

```ts
// получение 3-ех юзеров пропуская 3-х предыдущих юзеров (aka. пагинация)
const users: UsersResponse = await axios.get('/api/users?limit=3&offset=3');
```

## POST `/api/users`

Создание/регистрация юзера.

Если регистрация на страницу регистрации,
то после создания юзера - ему будет присвоена сессия с помомощью JWT токена,
которая помещается в куки на стороне сервера, а так же JWT токен сохраняется в базе,
чтобы БД удалила этот токен когда истечет время (сейчас стоит 1 день `JWT_EXPIRES_IN`)

```ts
export enum UserRole {
    ADMIN = 'admin',
    MASTER = 'master',
}

export type UserName = Tagged<string, 'UserId'>;

export type User = {
    username: UserName; // primary unique
    role: UserRole;
    createdAt: number; // timestamp
    firstName: string;
    lastName: string;
};

export type UserAuth = {
    username: UserName;
    password: string;
};

export type UserRegisterData = {
    auth: UserAuth;
    meta: Omit<User, 'createdAt'>;
};
```

```ts
// создание юзера
const user: User = await axios.post('/api/users', {
	auth: {
		username: 'some-username',
		password: '123456'
	},
	meta: {
		firstName: 'Some',
        lastName: 'Name',
	},
});
```

## POST `/api/users/login`

Авторизация юзера

Если данные верны ему будет присвоена сессия с помомощью JWT токена,
которая помещается в куки на стороне сервера, а так же JWT токен сохраняется в базе,
чтобы БД удалила этот токен когда истечет время (сейчас стоит 1 день `JWT_EXPIRES_IN`)

```ts
export type UserAuth = {
    username: UserName;
    password: string;
};
```
```ts
// авторизация юзера и получение его мета данных
const user: User = await axios.post('/api/users/login', {
	username: 'some-username',
	password: '123456',
});
```

## GET `/api/users/logout`

Удаление сессии юзера и "выход"

Удаляется сессия из кук и БД

> должна быть авторизация
```ts
await axios.get('/api/users/logout');
```

## GET `/api/users/u/[username]`

Получение всей мета инфы (модель/интерфейс) о юзере

> должна быть авторизация
```ts
// получение мета данных юзера
const user: User = await axios.get(`/api/users/u/${username}`);
```

## DELETE `/api/users/u/[username]`

Удаление юзера.

В текущей реализации удалять юзер может только юзер с ролью "admin"
Удалять юзеров с ролью "admin" запрещено

> должна быть авторизация
```ts
await axios.delete(`/api/users/u/${username}`)
```

## PATCH `/api/users/u/[username]/password`

Изменение пароля для юзера

> должна быть авторизация
```ts
export type SetPasswordData = {
    username: UserAuth['password'],
    currentPassword: UserAuth['password'];
    password: UserAuth['password'];
    passwordRepeat: UserAuth['password'];
};
```

```ts
await axios.patch(`/api/users/u/${username}/password`, {
	username: 'some-username', // only admin
	currentPassword: '123456',
	password: '1234567',
	passwordRepeat: '1234567',
})
```

## GET `/api/engines`

Получение списка двигателей

> должна быть авторизация
```ts
export type EngineId = Tagged<string, 'EngineId'>;

export type EngineHumanId = Tagged<string, 'HumanId'>;

export type Engine = {
    id: EngineId; // uniq primary
    humanId: EngineHumanId; // uniq
    createdAt: number; // timestamp
    maxSpeedPm: number;
    power: number;
    nominalVoltage: number
    nominalCurrent: number,
    weight: number;
};

export type EnginesRequest = Pagination<User>;
export type EnginesResponse = PaginationResp<User>;
```

```ts
// получение 3-ех двигателей пропуская 3-х предыдущих двигателей в порядке "сначала новые" (aka. пагинация)
const users: EnginesResponse = await axios.get('/api/engines?limit=3&offset=3&order=DESC');
```

## POST `/api/engines`

Создание двигателя

> должна быть авторизация

```ts
// создание двигателя
const engine: Engine = await axios.post('/api/engines', {
	humanId: "13256",
    maxSpeedPm: 142141,
    power: 123,
    nominalVoltage: 123,
    nominalCurrent: 123,
    weight: 123,
});
```

GET `/api/engines/[engineId]`

Получение информации о двигателе

> должна быть авторизация

```ts
// получение мета данных юзера
const engine: Engine = await axios.get(`/api/engine/${engineId}`);
```

DELETE `/api/engines/[engineId]`

Удаление двигателя

> должна быть авторизация
```ts
await axios.delete(`/api/engines/${engineId}`)
```

GET `/api/engines/[engineId]/maintenances`

```ts
export enum RotorFaultReason {
    None = 'None',
    SquirrelCage = 'SquirrelCage',
    Other = 'Other',
}

export enum WildingRotorFaultReason {
    None = 'None',
    Overheat = 'Overheat',
    Break = 'Break',
    Other = 'Other',
}

export enum StatorFaultReason {
    None = 'None',
    Overheat = 'Overheat',
    Other = 'Other',
}

export enum WildingStatorFaultReason {
    None = 'None',
    Overheat = 'Overheat',
    Break = 'Break',
    Other = 'Other',
}

export enum BearingFaultReason {
    None = 'None',
    Expired = 'Expired',
    BigGap = 'BigGap',
    WearOn = 'WearOn',
    Other = 'Other',
}

export enum FanFaultReason {
    None = 'None',
    Clog = 'Clog',
    Contamination = 'Contamination',
    Other = 'Other',
}

export type MaintenanceID = Tagged<string, 'MaintenanceID'>;

export type Maintenance = {
    id: MaintenanceID;
    engineId: EngineId;
    autor: UserName;
    createdAt: number;

    rotor: RotorFaultReason;
    rotorDescription?: string;

    wildingRotor: WildingRotorFaultReason;
    wildingRotorDescription?: string;

    wildingStator: WildingStatorFaultReason;
    wildingStatorDescription?: string;

    stator: StatorFaultReason;
    statorDescription?: string;

    bearing: BearingFaultReason;
    bearingDescription?: string;

    fan: FanFaultReason;
    fanDescription?: string;

    carriedOutDescription: string;
};
```

POST `/api/engines/[engineId]/maintenances`
GET `/api/engines/[engineId]/maintenances/[maintenanceId]`
