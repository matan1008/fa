def run(segments, manner, manner_args, addresses, args, **kwargs):
    return [ea + eval(args) for ea in addresses]
