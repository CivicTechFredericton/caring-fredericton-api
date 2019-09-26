from core.resource import ma


class RootSchema(ma.Schema):
    _links = ma.Hyperlinks({})

    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)

        rule_endpoints = {}
        for rule in app.url_map.iter_rules():
            if rule.arguments:
                continue

            endpoint = rule.endpoint.split('.')[0]
            rule_endpoints[endpoint] = ma.URLFor(rule.endpoint)

        self.fields['_links'].schema.update(rule_endpoints)
