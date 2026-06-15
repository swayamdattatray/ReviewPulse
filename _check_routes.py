from app import create_app

app = create_app()
with app.app_context():
    for rule in sorted(app.url_map.iter_rules(), key=lambda r: r.rule):
        methods = sorted(rule.methods - {"OPTIONS", "HEAD"})
        print(f"  {', '.join(methods):8s} {rule.rule}")
