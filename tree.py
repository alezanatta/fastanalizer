import sqlite3
import os

import plotly.graph_objects as go
import igraph

from Bio import AlignIO
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor

def convert_to_igraph(tree):
    #Convert a Biopython Tree object to an igraph Graph.
    def add_edge(graph, node1, node2):
        graph.add_edge(node1.name, node2.name)

    def build_subgraph(graph, top):
        """Traverse  the Tree, and retrieve  graph edges and nodes."""
        for clade in top:
            graph.add_vertex(name=clade.root.name)
            add_edge(graph, top.root, clade.root)
            build_subgraph(graph, clade)

    if tree.rooted:
        G = igraph.Graph(directed=True)
    else:
        G = igraph.Graph()
    G.add_vertex(name=str(tree.root))
    build_subgraph(G, tree.root)
    return G 

def nj_tree(BASE_DIR, tp_tree="NJ"):
    conn = sqlite3.connect(os.path.join(BASE_DIR, "fastanalizer.sqlite3"))
    cursor = conn.cursor()

    cursor.execute("""SELECT id, dsc_sequencia, cd_requisicao FROM pipeline_requisicao WHERE sn_align = True AND sn_error = False AND dt_conclusao IS NULL""")
    jobs = cursor.fetchall()

    for job in jobs:
        inner_node_color ='rgb(204, 204, 205)'
        node_color = "blue"

        if not os.path.exists(os.path.join(job[2], "align")):
            print("Pasta não existe: {}".format(job[2]))
            continue    
        if not os.path.exists(os.path.join(job[2], "tree")):
            os.makedirs(os.path.join(job[2], "tree"))

        aln = AlignIO.read(os.path.join(job[2], "align", "align.fasta"), 'fasta')
        calculator = DistanceCalculator('identity')
        dm = calculator.get_distance(aln)
        constructor = DistanceTreeConstructor()
        tree = constructor.nj(dm)

        with open(os.path.join(job[2], "tree", f"{job[2]}.tree"), "w") as arquivo:
            arquivo.write(str(tree))

        G=convert_to_igraph(tree)

        V =[v.index for v in G.vs]
        Edges=[e.tuple   for e in G.es]

        node_colors=[inner_node_color if 'Inner'  in v['name'] else node_color for v in G.vs]
        labels=[v['name']   for v in G.vs]
        display_labels=['' if 'Inner' in label else label for label in labels]
        node_size=[1 if d_label == '' else 7 for d_label in display_labels]

        layt=G.layout('kk')
        N=len(layt)

        Xn=[layt[k][0] for k in range(N)]
        Yn=[layt[k][1] for k in range(N)]

        Xe=[]
        Ye=[]
        for e in Edges:
            Xe+=[layt[e[0]][0],layt[e[1]][0], None]
            Ye+=[layt[e[0]][1],layt[e[1]][1], None]  

        trace1=go.Scatter(x=Xe,
                    y=Ye,
                    mode='lines',
                    line=go.Line(color=inner_node_color, width=1),
                    hoverinfo='none'
                    )
        trace2=go.Scatter(
                    x=Xn,
                    y=Yn,
                    mode='markers+text',
                    textposition='bottom center',
                    name='',
                    marker=go.Marker(symbol='circle',
                                    size=node_size, 
                                    color=node_colors,
                                    line=go.Line(color='rgb(50,50,50)', width=0.5)
                                    ),
                    text=display_labels,
                    hoverinfo='text',

                    )
        axis=dict(
                showline=False,  
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                title=''
            )

        layout = go.Layout(
            title="Bla", 
            width=800,
            height=800,
            showlegend=False,
            xaxis=go.XAxis(axis),
            yaxis=go.YAxis(axis),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            dragmode='drawopenpath',
            newshape_line_color='cyan',
            font_family="Roboto",
            
        margin=go.Margin(
            t=100
        ),
        hovermode='closest',
        annotations=go.Annotations([
            go.Annotation(
            showarrow=False, 
            text="Data source: [1]</a>",  
            xref='paper',     
            yref='paper',     
            x=0.2,  
            y=-0.1,  
            xanchor='left',   
            yanchor='bottom',  
            font=go.Font(
            size=14 
            )     
            )
            ]),
        )

        data=go.Data([trace1, trace2])
        fig=go.Figure(data=data, layout=layout)

        fig.update_layout(
            updatemenus = [
                dict(
                    type="buttons",
                    buttons = [
                        dict(
                            label="Show labels",
                            method="restyle",
                            args=[{"mode":"markers+text"}, [1]]
                        ),
                        dict(
                            label="Hide labels",
                            method="restyle",
                            args=[{"mode":"markers"}, [1]]
                        )
                    ]
                ),
                dict(
                    type="buttons",
                    buttons = [
                        dict(
                            label="Blue",
                            method="relayout",
                            args=[{"newshape_line_color":"blue"}, [1]]
                        ),
                        dict(
                            label="Cyan",
                            method="relayout",
                            args=[{"newshape_line_color":"cyan"}, [1]]
                        )
                    ]
                )
            ]
        )
        config = dict({'scrollZoom': True, 'modeBarButtonsToAdd':['drawline','drawopenpath','drawcircle','drawrect','eraseshape']}) 

        #fig.show(config=config)
        fig.write_html(os.path.join(job[2], "tree", "tree.html"))
