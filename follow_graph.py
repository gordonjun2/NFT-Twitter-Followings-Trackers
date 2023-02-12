import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import os

def create_follow_graph(follow_dict):

    '''
    'follow_dict' is in the following format, where the dictionary keys are the degens and
    then list values of each keys are the Twitter account each degen follows

    follow_dict = {
        'Gordon': {'NFT 1', 'NFT 3'}, 'Raven': {'NFT 1', 'NFT 2'} 
    }
    '''

    G = nx.Graph()
    for node, connections in follow_dict.items():
        for c in connections:
            G.add_edge(node, c)

    pos = nx.spring_layout(G)

    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append(str(adjacencies[0]) + ' (No. of connections: ' + str(len(adjacencies[1])) + ')')

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title='<b>Twitter Followings Graph</b>',
                    titlefont_size=20,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        text="Credits to Suryaveer Singh: <a href='https://stackoverflow.com/questions/49430040/how-to-avoid-overlapping-when-theres-hundreds-of-nodes-in-networkx'> https://stackoverflow.com/questions/49430040/how-to-avoid-overlapping-when-theres-hundreds-of-nodes-in-networkx/</a>",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )

    if not os.path.exists("followings_graph"):
        os.mkdir("followings_graph")

    fig.write_image("followings_graph/current_follow_graph.jpeg", width=1066, height=800)

    return fig

### Testing function ###

# sample_dict =   {'pranksy': 
#                     {'@cleandood', '@Rosewolf_artist', '@rebelstudios_io', '@_Goldenwolf_', 
#                     '@LostParadigms', '@jackbutcher', '@gabrielleydon', '@0xAndy_eth', '@futureverse' 
#                     }, 
#                 'SmartypantsNFT': 
#                     {'@coinmamba', '@degenpoet', '@PalantirVision', '@ProTheDoge', '@MomoguroNFT', 
#                     '@TateTheTalisman', '@ToysRUsNFT', '@ABC123Community', '@darenyoong', '@LtLollipop9' 
#                     }, 
#                 'talesrune': {'@symbiogenesisPR', '@pawwaoart', '@unfuddable', '@cryptoanon888', 
#                     '@SweeperSolana', '@traderhuey', '@ALEXGM__', '@226ETH_', '@_3noki3_', '@CryptoCapo_' 
#                     }, 
#                 'fiin9021': {'@DimensionalsRPG', '@daytonmills', '@Bonne_Syu', '@ExodiaGods', 
#                     '@MomoguroNFT', '@kaanayaz_', '@AlphaKingNFT_', '@OldeusOfficial', '@gabrielleydon' 
#                     }, 
#                 'SupremeGodGod': {'@xuedison3', '@Supers6061', '@nftboi_', '@SheckyLin', '@dreamfallart', 
#                     '@backendnft', '@NephalemNFT', '@ProjectZR_X', '@gabrielleydon', '@TENGOKU_HQ'
#                     }, 
#                 'pinseth': {'@MFHoz', '@gurgavin', '@FIMindset__', '@KUMALEON_', '@drugstore', '@CryptoPoseidonn', 
#                     '@unusual_whales', '@WatcherGuru', '@SnailySnailsNFT', '@skulourful', '@YakuzaFriday'
#                     }, 
#                 'kristopherlukas': {'@DimensionalsRPG', '@texturepunx', '@fudibles', 
#                     '@ShinseiVillage', '@Kyuu_bi_jima', '@HelpMeTradeThis', '@skwgmi', '@central_frog'
#                     }, 
#                 'cozypront': {'@zulpverse', '@SteezyPS', '@3uanNFT', '@shrimpgangsol', '@L4V107_NFT', '@mahesayoms', 
#                     '@StakeEddie', '@rigstertv', '@kimpossiblecpto', '@fresh0x', '@Jazz1x1', '@FrancoNFTS'
#                     }, 
#                 'EasyEatsBodega': {'@DimensionalsRPG', '@IronMike_13', 
#                     '@_timeless_relic', '@KingFlores150', '@evanluza', '@HakoiriOfficial', '@FakeJonnyy'
#                     }
#                 }

# fig = create_follow_graph(sample_dict)
# fig.show()