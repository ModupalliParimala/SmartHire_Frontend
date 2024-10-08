from dash.dependencies import Input, Output, State
import requests
from dash import html
import os

def generate_jd(app):
    @app.callback(
        [Output('output-state', 'children'),
         Output('download-link', 'children')],
        [Input('submit-button', 'n_clicks')],
        [State('job-title-input', 'value'), 
         State('experience-input', 'value'), 
         State('skill-input', 'value')]
    )
    def update_output(n_clicks, job_title, experience, skills):
        if n_clicks:
            api_url = os.getenv('SMARTHIRE_BACKEND_ENDPOINT')+'generate-jd'
            payload = {'job_title': job_title, 'experience': experience, 'skills': skills}
            
            try:
                response = requests.post(api_url, json=payload)
                response.raise_for_status()  # Raise an error if the request fails
                
                response_data = response.json()
                if response_data['status'] == '200':
                    filename = response_data['file_name']
                    download_link = html.A(
                        html.I(className='fas fa-download me-2'),
                        href=os.getenv('SMARTHIRE_BACKEND_ENDPOINT')+f'download?f_name={filename}&f_type=docx',
                        target='_blank',
                        className='btn btn-primary btn-sm'
                    )
                    return (
                        html.Div(
                            [
                                html.Div(
                                    f'File generated successfully: {filename}',
                                    className='alert alert-success d-flex align-items-center'
                                ),
                                download_link
                            ],
                            className='d-flex justify-content-between align-items-center'
                        ),
                        ''
                    )
                else:
                    return (
                        html.Div(
                            'Failed to generate file. Please try again.',
                            className='alert alert-danger'
                        ),
                        ''
                    )
            except requests.RequestException as e:
                return (
                    html.Div(
                        f'Error: {str(e)}',
                        className='alert alert-danger'
                    ),
                    ''
                )
        
        return '', ''
