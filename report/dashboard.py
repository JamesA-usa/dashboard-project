from fasthtml.common import *  # noqa F403
import matplotlib.pyplot as plt
import sys
from utils import load_model
"""
Below, we import the parent classes
you will use for subclassing
"""
from base_components import (
    Dropdown,
    BaseComponent,
    Radio,
    MatplotlibViz,
    DataTable
    )
from combined_components import FormGroup, CombinedComponent
root = Path(__file__).parent.parent / 'python-package'  # noqa F405
sys.path.append(root.as_posix())
from employee_events import Employee, Team  # noqa E402


class ReportDropdown(Dropdown):

    def build_component(self, entity_id, model):
        self.id = entity_id
        self.label = model.name
        return super().build_component(entity_id, model)

    def component_data(self, entity_id, model):

        names = model.names()
        self.options = [(name, id_) for name, id_ in names]
        return self.options


class Header(BaseComponent):
    def build_component(self, entity_id, model):
        return H1(model.name)  # noqa F405


class LineChart(MatplotlibViz):
    def visualization(self, entity_id, model):
        df = model.event_counts(entity_id)
        df = df.fillna(0)
        df = df.set_index('event_date')
        df = df.sort_index()
        df = df.cumsum(axis=0)
        df = df.rename(columns={'positive_events': 'Positive',
                                'negative_events': 'Negative'})

        fig, ax = plt.subplots()
        df.plot(ax=ax)
        self.set_axis_styling(ax, bordercolor='black', fontcolor='black')
        ax.set_title('Cumulative Event Counts', fontsize=20)
        ax.set_xlabel('Date', fontsize=15)
        ax.set_ylabel('Cumulative Count', fontsize=15)


class BarChart(MatplotlibViz):
    predictor = load_model()

    def visualization(self, entity_id, model):
        data = model.model_data(entity_id)
        proba = self.predictor.predict_proba(data)
        proba = proba[:, [1]]
        print(proba)
        if model.name == 'team':
            pred = proba.mean()
        else:
            pred = proba[0][0]
        print(pred)

        fig, ax = plt.subplots()
        ax.barh([''], [pred])
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_title('Predicted Recruitment Risk', fontsize=20)
        self.set_axis_styling(ax, bordercolor='black', fontcolor='black')


class Visualizations(CombinedComponent):
    children = [LineChart(), BarChart()]
    outer_div_type = Div(cls='grid')   # noqa F405


class NotesTable(DataTable):
    def component_data(self, entity_id, model):
        return model.notes(entity_id)


class DashboardFilters(FormGroup):

    id = "top-filters"
    action = "/update_data"
    method = "POST"

    children = [
        Radio(
            values=["Employee", "Team"],
            name='profile_type',
            hx_get='/update_dropdown',
            hx_target='#selector'
            ),
        ReportDropdown(
            id="selector",
            name="user-selection")
        ]


class Report(CombinedComponent):
    children = [Header(), DashboardFilters(), Visualizations(), NotesTable()]


app = FastHTML()  # noqa F405
report = Report()


@app.route('/')
def get():  # noqa F811
    return report(1, Employee())


@app.route('/employee/{id}')
def get(id: str):  # noqa F811
    return report(id, Employee())


@app.route('/team/{id}')
def get(id: str):  # noqa F811
    return report(id, Team())


@app.get('/update_dropdown{r}')
def update_dropdown(r):
    dropdown = DashboardFilters.children[1]
    print('PARAM', r.query_params['profile_type'])
    if r.query_params['profile_type'] == 'Team':
        return dropdown(None, Team())
    elif r.query_params['profile_type'] == 'Employee':
        return dropdown(None, Employee())


@app.post('/update_data')
async def update_data(r):
    from fasthtml.common import RedirectResponse
    data = await r.form()
    profile_type = data._dict['profile_type']
    id = data._dict['user-selection']
    if profile_type == 'Employee':
        return RedirectResponse(f"/employee/{id}", status_code=303)
    elif profile_type == 'Team':
        return RedirectResponse(f"/team/{id}", status_code=303)


serve()  # noqa F405
