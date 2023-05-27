def load(app, cognito_verifier=None, telemetry_agent=None):
  @app.route('/api/health-check')
  def health_check():
    return {'success': True, 'ver': 1}, 200