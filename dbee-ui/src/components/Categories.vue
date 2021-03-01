<template>
    <div>
        <b-container fluid>
            <div class="hello" ref="chartdiv"></div>        
            <h3>{{ chosenCategory }}</h3>
            <b-table
                striped:
                :fields="emailFields"
                :items="emailsRaw"
                @row-clicked="rowClickHandler"
                :tbody-td-class="cellClass"
                fixed responsive
            >
                <template #cell(sentiment)="data">
                    <b-icon icon="circle-fill" aria-hidden="true" :variant="sentimentStyle(data.item.sentiment)"></b-icon>            
                </template>
                <template #table-colgroup="scope">
                    <col
                    v-for="field in scope.fields"
                    :key="field.key"
                    :style="{ width: field.key === 'subject' ? '150px' : '180px' }"
                    >
                </template>
            </b-table>
        </b-container>
    </div>
</template>

<script>
import * as am4core from "@amcharts/amcharts4/core";
// import am4themes_kelly from "@amcharts/amcharts4/themes/kelly";
import am4themes_animated from "@amcharts/amcharts4/themes/animated";
import am4themes_dark from "@amcharts/amcharts4/themes/dark";
import * as am4plugins_forceDirected from "@amcharts/amcharts4/plugins/forceDirected";

import axios from 'axios'

am4core.useTheme(am4themes_animated);
// am4core.useTheme(am4themes_kelly);
am4core.useTheme(am4themes_dark);

export default {
    name: "Categories",
    mounted() {        
        this.getCategoryWeights()
    },
    beforeDestroy() {
        if (this.chart) {
        this.chart.dispose();
        }
    },
    methods: {
        sentimentStyle(sentiment) {
            return (sentiment > 0.25) ? 'success' : (sentiment < -0.25) ? 'danger' : 'warning'
        },
        rowClickHandler(record) {
            const h = this.$createElement
            // Using HTML string
            const titleVNode = h('div', { domProps: { innerHTML: 'Subject: ' + record.subject } })
            // More complex structure
            const messageVNode = h('div', { class: ['foobar'] }, [
                h('strong', 'From: '),
                h('p',[record.from]),
                h('strong', 'Message: '),
                h('p',[record.text]),
                // h('b-button', {
                //     props: {
                //     variant: "danger",
                //     click: "callTextToVoice()"
                //     }
                // })
            ])
            // We must pass the generated VNodes as arrays
            this.$bvModal.msgBoxOk([messageVNode], {
            title: [titleVNode],
            buttonSize: 'sm',
            centered: true, size: 'lg'
            })
        },
        callTextToVoice: function() {
            console.log("test")
        },
        getCategoryWeights:function() {
                axios
                    .get('/api-categories')
                    .then(response => (this.categoryWeights = response.data))
                    .then(() => this.displayCategoriesDiagramme())
        },
        getEmails:function(category) {
                axios
                    .get('/api-emails-1', { params: { category: category } })
                    .then(response => {
                        this.emailsRaw = response.data
                        this.emails = []
                        response.data.forEach(email => {
                            let emailItem = {}
                            emailItem["from"] = email.from
                            emailItem["subject"] = email.subject
                            this.emails.push(emailItem)
                        })
                    } )
        },
        displayCategoriesDiagramme: function() {
            let chart = am4core.create(this.$refs.chartdiv, am4plugins_forceDirected.ForceDirectedTree);
        
            var networkSeries = chart.series.push(new am4plugins_forceDirected.ForceDirectedSeries())

            var data = this.categoryWeights

            chart.data = data;

            networkSeries.dataFields.value = "score";
            networkSeries.dataFields.name = "category";
            networkSeries.dataFields.children = "children";
            networkSeries.nodes.template.tooltipText = "{name}:{value}";
            networkSeries.nodes.template.fillOpacity = 1;
            networkSeries.dataFields.id = "name";
            networkSeries.dataFields.linkWith = "linkWith";
            networkSeries.nodes.template.label.text = "{name}"
            networkSeries.fontSize = 18

            var label = chart.createChild(am4core.Label);
            label.x = 50;
            label.y = 50;
            label.isMeasured = false;

            this.chart = chart;

            networkSeries.nodes.template.events.on("up", processCategory, this)

            function processCategory(event) {
                this.chosenCategory = event.target.label.currentText
                this.getEmails(event.target.label.currentText)
            }       
        }
    },
    data() {
        return {
            "categoryWeights": [],
            "emails": [],
            "emailsRaw": [],
            "chosenCategory": "",
            "emailFields": [
                {key: "subject"},
                {key: "from"},
                {key: "sentiment", sortable: true}
            ]
        }
    }
}
</script>

<style scoped>
.hello {
  width: 100%;
  height: 500px;
}
td {
   max-width: 200px;
}
</style>