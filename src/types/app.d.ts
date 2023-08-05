type allSchedule = {
    'data'?: {
        '0': {
            'today': {
                'group': {
                    '0': '',
                    '1': '',
                    '2': '',
                    '3': '',
                    '4': '',
                    '5': '',
                    '6': '',
                },
            },
        },
        '1': {
            'next_day': {
                'group': {
                    '0': '',
                    '1': '',
                    '2': '',
                    '3': '',
                    '4': '',
                    '5': '',
                    '6': '',
                },
            },

        }
    }
} 

type MAXIMUM_ALLOWED_BOUNDARY = 6

type ComputeRange<
    N extends number,
    Result extends Array<unknown> = [],
> =
    (Result['length'] extends N
        ? Result
        : ComputeRange<N, [...Result, Result['length']]>
    )

// 0 , 1, 2 ... 998
type NumberRange = ComputeRange<MAXIMUM_ALLOWED_BOUNDARY>[number]

type Name<T extends string> = { name: T }

type CustomResponse = {
    [Prop in NumberRange]: Record<`random id${Prop}`, Name<`id${Prop}`>>
}