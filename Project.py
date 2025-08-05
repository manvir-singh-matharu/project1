import plotly.express as px
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import json
import folium 



data = pd.read_csv("combinedemploymentdatafinal.csv")


df = pd.DataFrame(data)


st.title("Employment Data Dashboard")


regionforbar = df.groupby("Region")[["Urban_Employability(%)", "Rural_Employability(%)"]].mean().reset_index()

fig1 = px.bar(
    regionforbar,
    x="Region",
    y=["Urban_Employability(%)", "Rural_Employability(%)"],
    title="Comparison of Urban and Rural Employability by Region",
    barmode="group",
    labels={"value": "Employability (%)", "variable": "Employment Type"}
)



regionforpie = df.groupby("Region")[["Graduate(%)"]].mean().reset_index()

fig2 = px.pie(
    regionforpie,
    values="Graduate(%)",
    names="Region",
    title="Average Percentage of Graduates by Region"
)



agegroupcomp = df.groupby("Region")[["Age_Group_18_25(%)", "Age_Group_26_35(%)"]].mean().reset_index()

agegroupmelt = agegroupcomp.melt(id_vars="Region", var_name="Age Group", value_name="Average Employability (%)")

fig3=px.bar(
    agegroupmelt,
    x="Region",
    y="Average Employability (%)",
    color="Age Group",
    title="Average Employability by Age Group and Region",
    barmode="group"
)


fig4= go.Figure(data=[
    go.Bar(name="Male Employability", x=df["State Name"], y=df["Male_Employability(%)"]),
    go.Bar(name="Female Employability", x=df["State Name"], y=df["Female_Employability(%)"])
])
fig4.update_layout(
    title="Gender-wise Employability by State/UT",
    xaxis_title="State/UT",
    yaxis_title="Employability (%)",
    barmode="group"
)



sectoremp = df[["State Name", "Service_Sector(%)", "Manufacturing_Sector(%)", "Agriculture_Sector(%)"]]


sectorempmelt = sectoremp.melt(id_vars="State Name", var_name="Sector", value_name="Employability (%)")


fig5 = px.bar(
    sectorempmelt,
    x="State Name",
    y="Employability (%)",
    color="Sector",
    title="Sector-wise Employability by State/UT"
)

fig5.update_layout(
    xaxis_title="State/UT",
    yaxis_title="Employability (%)",
    barmode="stack"
)



qualification=df.melt(id_vars="State Name", value_vars=["Graduate(%)", "ITI(%)", "Diploma(%)"], var_name="Qualification", value_name="Percentage")

fig6=px.sunburst(
    qualification,
    path=["Percentage","State Name", "Qualification"],
    values="Percentage",
    title="Qualification Distribution by State/UT"
)

df["Overall Employability (%)"] = df[["Urban_Employability(%)", "Rural_Employability(%)", "Male_Employability(%)","Female_Employability(%)"]].mean(axis=1)

with open("newindia.json") as f:
    map_data = json.load(f)
m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

for feature in map_data["features"]:
    print(feature["properties"]["st_nm"])

snm = {
    "Delhi": "NCT of Delhi",
    "Pondicherry": "Puducherry",
    "Odisha": "Orissa",
}

df["State Name"] = df["State Name"].replace(snm)


fig7 = px.choropleth_mapbox(
    df,
    geojson=map_data,
    locations="State Name",
    featureidkey="properties.st_nm",  # Critical fix here
    color="Overall Employability (%)",
    mapbox_style="carto-positron",
    zoom=3,
    center={"lat": 20.5937, "lon": 78.9629},
    opacity=0.5,
    title="Overall Employability by State/UT"
)

chartcategories={
    "Demographics": ["Urban Employability", "Rural Employability", "Age Group Employability","Overall Employability"],
    "Education": ["Graduate Employability", "Qualification Distribution"],
    "Industry":["Sector-wise Employability"]

}
selected_category = st.sidebar.selectbox("Select Category", list(chartcategories.keys()))
selected_chart = st.sidebar.selectbox("Select Chart", chartcategories[selected_category])



if selected_chart == "Urban Employability":
    st.plotly_chart(fig1, key="fig1")
elif selected_chart == "Rural Employability":
    st.plotly_chart(fig2, key="fig2")
elif selected_chart == "Age Group Employability":
    st.plotly_chart(fig3, key="fig3")
elif selected_chart == "Graduate Employability":
    st.plotly_chart(fig4, key="fig4")
elif selected_chart == "Sector-wise Employability":
    st.plotly_chart(fig5, key="fig5")
elif selected_chart == "Qualification Distribution":
    st.plotly_chart(fig6, key="fig6")
elif selected_chart == "Overall Employability":
    st.plotly_chart(px.choropleth_mapbox(
        df,
        geojson=map_data,
        locations="State Name",
        color="Overall Employability (%)",
        mapbox_style="carto-positron",
        zoom=3,
        center={"lat": 20.5937, "lon": 78.9629},
        opacity=0.5,
        title="Overall Employability by State/UT"
    ), use_container_width=True, key="fig7")
