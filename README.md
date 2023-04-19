# PICO-8 Gymn

## Reinforcement Learning package for PICO-8 games

### Websocket Communications

#### From Client

- Console Initialized

```
{
    'event': 'init'
}
```

- Reset Confirmed

```
{
    'event': 'reset'
}
```

- Step Response

```
{
    'step': $INT
    'observation': {
        'screen': '$BASE64_IMG_STRING'
    },
    'reward': $FLOAT,
    'terminated': $BOOL,
    'truncated': $BOOL,
    'info': $DICT
}
```

#### From Server

- Reset Stage

```
{
    'commands': [
        {
            'type': 'reset',
            'seed': $INT,
            **options
        }
    ]
}
```

- Step Input

```
{
    'step': $INT,
    'input': [
        $LEFT_KEY,
        $RIGHT_KEY,
        $UP_KEY,
        $DOWN_KEY,
        $O_KEY,
        $X_KEY
    ],
    'commands': [
        {
            'type': '$COMMAND_TYPE',
            **options
        }
    ]
}
```