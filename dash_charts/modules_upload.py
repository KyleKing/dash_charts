"""Upload module and helpers for managing file upload and download.

Some functions based on code from:
https://docs.faculty.ai/user-guide/apps/examples/dash_file_upload_download.html

"""

import base64
import io
import json
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import quote as urlquote

import dash_bootstrap_components as dbc
import pandas as pd
from dash import dash_table, dcc, html

from .utils_app_modules import ModuleBase
from .utils_callbacks import map_args, map_outputs
from .utils_dataset import DBConnect
from .utils_json_cache import CACHE_DIR


def split_b64_file(b64_file):
    """Separate the data type and data content from a b64-encoded string.

    Args:
        b64_file: file encoded in base64

    Returns:
        tuple: of strings `(content_type, data)`

    """
    return b64_file.encode('utf8').split(b';base64,')


def save_file(dest_path, b64_file):
    """Decode and store a file uploaded with Plotly Dash.

    Args:
        dest_path: Path on server filesystem to save the file
        b64_file: file encoded in base64

    """
    data = split_b64_file(b64_file)[1]
    dest_path.write_text(base64.decodebytes(data).decode())


def uploaded_files(upload_dir):
    """List the files in the upload directory.

    Args:
        upload_dir: directory where files are uploadedfolder

    Returns:
        list: Paths of uploaded files

    """
    return [*upload_dir.glob('*.*')]


def file_download_link(filename):
    """Create a Plotly Dash 'A' element that when clicked triggers a file downloaded.

    Args:
        filename: Path to local file to be available for user download

    Returns:
        html.A: clickable Dash link to trigger download

    """
    # PLANNED: Revisit. Should filename be a name or the full path?
    return html.A(filename, href=f'/download/{urlquote(filename)}')


def parse_uploaded_image(b64_file, filename, timestamp):
    """Create an HTML element to show an uploaded image.

    Args:
        b64_file: file encoded in base64
        filename: filename of upload file. Name only
        timestamp: upload timestamp

    Returns:
        html.Img: if image data type

    Raises:
        RuntimeError: if filetype is not a supported image type

    """
    content_type, data = split_b64_file(b64_file)
    if 'image' not in content_type:
        raise RuntimeError(f'Not image type. Found: {content_type}')
    return html.Img(src=b64_file)


def parse_json(raw_json):
    """Return dataframe from JSON formatted in the 'records' orientation.

    Args:
        raw_json: json string

    Returns:
        dataframe: uploaded dataframe parsed from JSON

    Raises:
        RuntimeError: if the JSON file can't be parsed

    """
    dict_json = json.loads(raw_json)
    keys = [*dict_json.keys()]
    if len(keys) != 1:
        raise RuntimeError(
            'Expected JSON with format `{data: [...]}` where `data` could be any key.'
            f'However, more than one key was found: {keys}',
        )
    return pd.DataFrame.from_records(dict_json[keys[0]])


def load_df(decoded, filename):
    """Identify file type and parse the uploaded content into a dataframe.

    Args:
        decoded: string contents/data of the file decoded from the full base64 file
        filename: filename of upload file. Name only

    Returns:
        dataframe: uploaded dataframe parsed from source file

    Raises:
        RuntimeError: if file suffix suffix is unsupported

    """
    suffix = Path(filename).suffix.lower()
    if suffix == '.csv':
        df_upload = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

    elif suffix.startswith('.xl'):
        # xlsx will have 'spreadsheet' in `content_type` but xls will not have anything
        df_upload = pd.read_excel(io.BytesIO(decoded))

    elif suffix == '.json':
        df_upload = parse_json(decoded.decode('utf-8'))

    else:
        raise RuntimeError(f'File type ({suffix}) is unsupported. Expected .csv, .xl*, or .json')

    return df_upload  # noqa: R504


def parse_uploaded_df(b64_file, filename, timestamp):
    """Decode base64 data and parse based on file type. Attempts to return the parsed data as a Pandas dataframe.

    Args:
        b64_file: file encoded in base64
        filename: filename of upload file. Name only
        timestamp: upload timestamp

    Returns:
        dataframe: pandas dataframe parsed from source file

    Raises:
        RuntimeError: if raw data could not be parsed

    """
    content_type, data = split_b64_file(b64_file)
    decoded = base64.b64decode(data)
    try:
        df_upload = load_df(decoded, filename)

    except Exception as error:
        raise RuntimeError(f'Could not parse {filename} ({content_type})\nError: {error}')

    return df_upload  # noqa: R504


def show_toast(message, header, icon='warning', style=None, **toast_kwargs):
    """Create toast notification.

    Args:
        message: string body text
        header: string notification header
        icon: string name in `(primary,secondary,success,warning,danger,info,light,dark)`. Default is warning
        style: style dictionary. Default is the top right
        toast_kwargs: additional toast keyword arguments (such as `duration=5000`)

    Returns:
        dbc.Toast: toast notification from Dash Bootstrap Components library

    """
    if style is None:
        # Position in the top right (note: will occlude the tabs when open, could be moved elsewhere)
        style = {'position': 'fixed', 'top': 10, 'right': 10, 'width': 350, 'zIndex': 1900}
    return dbc.Toast(message, header=header, icon=icon, style=style, dismissable=True, **toast_kwargs)


def drop_to_upload(**upload_kwargs):
    """Create drop to upload element. Dashed box of the active area or a clickable link to use the file dialog.

    Based on dash documentation from: https://dash.plotly.com/dash-core-components/upload

    Args:
        upload_kwargs: keyword arguments for th dcc.Upload element. Children and style are reserved

    Returns:
        dcc.Upload: Dash upload element

    """
    return dcc.Upload(
        children=html.Div(['Drag and Drop or ', html.A('Select a File')]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px',
        },
        **upload_kwargs,
    )


class UploadModule(ModuleBase):  # noqa: H601
    """Module for user data upload.

    Note: this is not intended to be secure

    """

    id_upload = 'upload-drop-area'
    """Unique name for the upload component."""

    id_upload_output = 'upload-output'
    """Unique name for the div to contain output of the parse-upload."""

    id_username_cache = 'username-cache'
    """Unique name for the dcc.Store element to store the current username."""

    all_ids = [id_upload, id_upload_output, id_username_cache]
    """List of ids to register for this module."""

    cache_dir = CACHE_DIR
    """Path to the directory to use for caching files."""

    def __init__(self, *args, **kwargs):
        """Initialize module."""  # noqa: DAR101
        super().__init__(*args, **kwargs)
        self._initialize_database()

    def _initialize_database(self):
        """Create data members `(self.database, self.user_table, self.inventory_table)`."""
        self.database = DBConnect(self.cache_dir / f'_placeholder_app-{self.name}.db')
        self.user_table = self.database.db.create_table(
            'users', primary_id='username', primary_type=self.database.db.types.text,
        )
        self.inventory_table = self.database.db.create_table(
            'inventory', primary_id='table_name', primary_type=self.database.db.types.text,
        )

    def find_user(self, username):
        """Return the database row for the specified user.

        Args:
            username: string username

        Returns:
            dict: for row from table or None if no match

        """
        return self.user_table.find_one(username=username)

    def add_user(self, username):
        """Add the user to the table or update the user's information if already registered.

        Args:
            username: string username

        """
        now = time.time()
        if self.find_user(username):
            self.user_table.upsert({'username': username, 'last_loaded': now}, ['username'])
        else:
            self.user_table.insert({'username': username, 'creation': now, 'last_loaded': now})

    def upload_data(self, username, df_name, df_upload):
        """Store dataframe in database for specified user.

        Args:
            username: string username
            df_name: name of the stored dataframe
            df_upload: pandas dataframe to store

        Raises:
            Exception: If upload fails, deletes the created table

        """
        now = time.time()
        table_name = f'{username}-{df_name}-{int(now)}'
        table = self.database.db.create_table(table_name)
        try:
            table.insert_many(df_upload.to_dict(orient='records'))
        except Exception:
            table.drop()  # Delete the table if upload fails
            raise

        self.inventory_table.insert({
            'table_name': table_name, 'df_name': df_name, 'username': username,
            'creation': now,
        })

    def get_data(self, table_name):
        """Retrieve stored data for specified dataframe name.

        Args:
            table_name: unique name of the table to retrieve

        Returns:
            pd.DataFrame: pandas dataframe retrieved from the database

        """
        table = self.database.db.load_table(table_name)
        return pd.DataFrame.from_records(table.all())

    def delete_data(self, table_name):
        """Remove specified data from the database.

        Args:
            table_name: unique name of the table to delete

        """
        self.database.db.load_table(table_name).drop()

    def return_layout(self, ids):
        """Return the Upload module application layout.

        Args:
            ids: `self._il` from base application

        Returns:
            dict: Dash HTML object.

        """
        return html.Div([
            dcc.Store(id=ids[self.get(self.id_username_cache)], storage_type='session'),
            html.H2('File Upload'),
            html.P('Upload Tidy Data in CSV, Excel, or JSON format'),
            drop_to_upload(id=ids[self.get(self.id_upload)]),
            dcc.Loading(html.Div('', id=ids[self.get(self.id_upload_output)]), type='circle'),
        ])

    def create_callbacks(self, parent):
        """Register callbacks to handle user interaction.

        Args:
            parent: parent instance (ex: `self`)

        """
        super().create_callbacks(parent)
        self.register_upload_handler(parent)

    def _show_data(self, username):
        """Create Dash HTML to show the raw data loaded for the specified user.

        Args:
            username: string username

        Returns:
            dict: Dash HTML object

        """
        # TODO: Add delete button for each table - need pattern matching callback:
        #   https://dash.plotly.com/pattern-matching-callbacks
        def format_table(df_name, username, creation, raw_df):
            user_str = f'by "{username}" ' if username else ''
            return [
                html.H4(df_name),
                html.P(f'Uploaded {user_str}on {datetime.fromtimestamp(creation)} (Note: only first 10 rows & 10 col)'),
                dash_table.DataTable(
                    data=raw_df[:10].to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in raw_df.columns[:10]],
                    style_cell={
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                        'maxWidth': 0,
                    },
                ),
                html.Hr(),
            ]

        children = [html.Hr()]
        rows = self.inventory_table.find(username=username)
        for row in sorted(rows, key=lambda _row: _row['creation'], reverse=True):
            df_upload = self.get_data(row['table_name'])
            children.extend(format_table(row['df_name'], row['username'], row['creation'], df_upload))
        return html.Div(children)

    def register_upload_handler(self, parent):
        """Register callbacks to handle user interaction.

        Args:
            parent: parent instance (ex: `self`)

        """
        outputs = [(self.get(self.id_upload_output), 'children')]
        inputs = [(self.get(self.id_upload), 'contents'), (self.get(self.id_username_cache), 'data')]
        states = [(self.get(self.id_upload), 'filename'), (self.get(self.id_upload), 'last_modified')]

        @parent.callback(outputs, inputs, states, pic=True)
        def upload_handler(*raw_args):
            a_in, a_state = map_args(raw_args, inputs, states)
            b64_file = a_in[self.get(self.id_upload)]['contents']
            username = a_in[self.get(self.id_username_cache)]['data']
            filename = a_state[self.get(self.id_upload)]['filename']
            timestamp = a_state[self.get(self.id_upload)]['last_modified']

            child_output = []
            try:
                if b64_file is not None:
                    df_upload = parse_uploaded_df(b64_file, filename, timestamp)
                    df_upload = df_upload.dropna(axis='columns')  # FIXME: Better handle NaN values...
                    self.add_user(username)
                    self.upload_data(username, filename, df_upload)

            except Exception as error:
                child_output.extend([
                    show_toast(f'{error}', 'Upload Error', icon='danger'),
                    dcc.Markdown(f'### Upload Error\n\n{type(error)}\n\n```\n{error}\n```'),
                ])

            child_output.append(self._show_data(username))

            return map_outputs(outputs, [(self.get(self.id_upload_output), 'children', html.Div(child_output))])
