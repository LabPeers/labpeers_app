from pylab import figure, axes, pie, title
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot

def test_matplotlib(request):
    f = figure(1, figsize=(6,6))
    ax = axes([0.1, 0.1, 0.8, 0.8])
    labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
    fracs = [15,30,45, 10]
    explode=(0, 0.05, 0, 0)
    pie(fracs, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True)
    title('Raining Hogs and Dogs', bbox={'facecolor':'0.8', 'pad':5})

    canvas = FigureCanvasAgg(f)    
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response
    matplotlib.pyplot.close(f)



    