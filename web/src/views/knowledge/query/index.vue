<!--
 * @Descripttion: 
 * @version: 0.x
 * @Author: zhai
 * @Date: 2024-06-02 20:09:52
 * @LastEditors: zhai
 * @LastEditTime: 2024-06-12 22:00:35
-->

<template>
    <div class="h-full">
        <n-radio-group v-model:value="curlayout" @update:value="onLayoutChange">
            <n-radio-button v-for="lay in layoutnames" :key="lay.value" :value="lay.value">
                {{ lay.label }}
            </n-radio-button>
        </n-radio-group>
        <div class="my-line-style-1">
            <relation-graph ref="graphRef" :options="graphOptions" @canvas-click="onCanvasClick"
                @node-click="onNodeClick" @line-click="onLineClick">
                <!-- <template #node="{ node }">
                <div @mouseover="showNodeTips(node, $event)" @mouseout="hideNodeTips(node, $event)">
                    <div class="c-my-rg-node">
                        <i style="font-size: 30px;" :class="node.data.myicon" />
                    </div>
                    <div
                        style="color: forestgreen;font-size: 16px;position: absolute;width: 160px;height:25px;line-height: 25px;margin-top:5px;margin-left:-48px;text-align: center;background-color: rgba(66,187,66,0.2);">
                        {{ node.data.myicon }}
                    </div>
                </div>
            </template> -->
            </relation-graph>

        </div>
    </div>

</template>

<script lang="ts" setup>
import { onMounted, reactive, ref } from 'vue';
import RelationGraph from 'relation-graph/vue3';
import type { RGJsonData, RGNode, RGLine, RGLink, RGUserEvent, RGOptions, RelationGraphComponent } from 'relation-graph-vue3';


const graphRef = ref<RelationGraphComponent | null>(null);

// 'layout': {
//         'layoutName': 'tree',
//         'min_per_width': 40,
//         'max_per_width': 70,
//         'min_per_height': 200
//     },
// layout: {
//       layoutName: 'force'
//     },
const curlayout = ref("中心布局");
const layoutnames = ref([
    { value: 0, label: "中心布局" },
    { value: 1, label: "树状布局" },
    { value: 2, label: "力学布局" }
]);

const layouts = (
    {
        "中心布局":
        {
            layout: {
                layoutName: 'center',
                centerOffset_x: 0,
                centerOffset_y: 0,
                distance_coefficient: 1,
                from: "top",
                levelDistance: "",
                min_per_width: 100,
                max_per_width: 500,
                min_per_height: 300,
                max_per_height: 500,
                maxLayoutTimes: 300,
                force_node_repulsion: 1,
                force_line_elastic: 1
            },
            debug: false,
            defaultNodeBorderWidth: 0,
            allowSwitchLineShape: true,
            allowSwitchJunctionPoint: true,
            defaultLineShape: 1,
            defaultFocusRootNode: false,

            moveToCenterWhenRefresh: true,
            useAnimationWhenRefresh: true,
            zoomToFitWhenRefresh: true,

            defaultExpandHolderPosition: 'bottom',
            reLayoutWhenExpandedOrCollapsed: true,
            useAnimationWhenExpanded: true,

            defaultJunctionPoint: 'border',
            defaultNodeColor: 'rgb(29, 169, 245)',
            defaultLineColor: 'rgb(29, 169, 245)',
        }
        ,
        "树状布局":
        {
            layout: {
                layoutName: 'tree'
            },
            // layoutClassName: 'seeks-layout-center',
            // useLayoutStyleOptions: true,
            // from: 'top',
            // defaultNodeWidth: 30,
            // defaultNodeHeight: 100,
            // defaultJunctionPoint: 'tb',
            // defaultNodeShape: 1,
            // defaultLineShape: 4,
            // defaultNodeBorderWidth: 0,
            // defaultLineColor: 'rgba(0, 186, 189, 1)',
            // defaultNodeColor: 'rgba(0, 206, 209, 1)',
            // min_per_width: 40,
            // max_per_width: 70,
            // min_per_height: 200

        },
        "力学布局":
        {
            layout: {
                layoutName: 'force'
            },
            // layoutClassName: 'seeks-layout-center',
            // useLayoutStyleOptions: true,
            // from: 'left',
            // defaultNodeWidth: 100,
            // defaultNodeHeight: 30,
            // defaultJunctionPoint: 'lr',
            // defaultNodeShape: 1,
            // defaultLineShape: 3,
            // defaultNodeBorderWidth: 0,
            // defaultLineColor: '#cccccc',
            // defaultNodeColor: '#43a2f1',
            // min_per_width: 200,
            // max_per_width: 400,
            // min_per_height: 40,
            // max_per_height: 70
        }
    });

async function onLayoutChange(lay) {
    // graphOptions.value.layout.layoutName = "tree";
    const graphInstance = graphRef.value.getInstance();
    // graphInstance.setOptions(layouts[lay]);
    graphInstance.switchLayout(graphOptions.layouts[lay]);

    await graphInstance.moveToCenter();
    await graphInstance.zoomToFit();
}

// const graphOptions: RGOptions = {
//     debug: false,
//     defaultNodeBorderWidth: 0,
//     allowSwitchLineShape: true,
//     allowSwitchJunctionPoint: true,
//     defaultLineShape: 1,
//     defaultFocusRootNode: false,

//     moveToCenterWhenRefresh: true,
//     useAnimationWhenRefresh: true,
//     zoomToFitWhenRefresh: true,

//     defaultExpandHolderPosition: 'bottom',
//     reLayoutWhenExpandedOrCollapsed: true,
//     useAnimationWhenExpanded: true,

//     layout: {
//         layoutName: 'center'
//     },

//     defaultJunctionPoint: 'border',
//     defaultNodeColor: 'rgb(29, 169, 245)',
//     defaultLineColor: 'rgb(29, 169, 245)',
// };

const graphOptions: RGOptions = {
    allowSwitchLineShape: true,
    allowSwitchJunctionPoint: true,
    toolBarVersion: 'v1',
    layouts: [
        {
            label: '中心布局',
            layoutName: 'center',
            layoutClassName: 'seeks-layout-center',
            useLayoutStyleOptions: true,
            defaultNodeWidth: 50,
            defaultNodeHeight: 50,
            defaultNodeBorderWidth: 0,
            defaultNodeColor: 'rgba(238, 178, 94, 1)',
            defaultLineShape: 1

        },
        {
            label: '树状布局',
            layoutName: 'tree',
            layoutClassName: 'seeks-layout-center',
            useLayoutStyleOptions: true,
            from: 'top',
            defaultNodeWidth: 30,
            defaultNodeHeight: 100,
            defaultJunctionPoint: 'tb',
            defaultNodeShape: 1,
            defaultLineShape: 4,
            defaultNodeBorderWidth: 0,
            defaultLineColor: 'rgba(0, 186, 189, 1)',
            defaultNodeColor: 'rgba(0, 206, 209, 1)',
            min_per_width: 40,
            max_per_width: 70,
            min_per_height: 200

        },
        {
            label: '布局3',
            layoutName: 'force',
            layoutClassName: 'seeks-layout-center',
            useLayoutStyleOptions: true,
            from: 'left',
            defaultNodeWidth: 100,
            defaultNodeHeight: 30,
            defaultJunctionPoint: 'lr',
            defaultNodeShape: 1,
            defaultLineShape: 3,
            defaultNodeBorderWidth: 0,
            defaultLineColor: '#cccccc',
            defaultNodeColor: '#43a2f1',
            min_per_width: 200,
            max_per_width: 400,
            min_per_height: 40,
            max_per_height: 70

        }
    ],
    defaultJunctionPoint: 'border'
};

onMounted(() => {
    showGraph();
});


const isShowNodeTipsPanel = ref(false);
const nodeMenuPanelPosition = ref({ x: 0, y: 0 });
const currentNode = ref({});

const showNodeTips = (nodeObject, $event) => {
    currentNode.value = nodeObject;
    const _base_position = myPage.value.getBoundingClientRect();
    console.log('showNodeMenus:', $event.clientX, $event.clientY, _base_position);
    isShowNodeTipsPanel.value = true;
    nodeMenuPanelPosition.value.x = $event.clientX - _base_position.x + 10;
    nodeMenuPanelPosition.value.y = $event.clientY - _base_position.y + 10;
};

const hideNodeTips = (nodeObject, $event) => {
    isShowNodeTipsPanel.value = false;
};

// const onSizeOptionChanged = () => {
//     myGraphPanelSize.value.width = currentSize.value;
//     myGraphPanelSize.value.height = currentSize.value;
//     nextTick(() => {
//         const graphInstance = graphRef.value.getInstance();
//         graphInstance.refresh();
//     });
// };


const onNodeClick = (nodeObject: RGNode, $event: RGUserEvent) => {

    // graphRef.value.getNodes().forEach((item) => {
    //     if (item.id != nodeObject.id) {
    //         item.opacity = 0.1;
    //     } else {
    //         item.opacity = 1;
    //     }
    // });
    // graphRef.value.getLines().forEach((item) => {
    //     item.relations.forEach((line) => {
    //         if (item.toNode.id == nodeObject.id || item.fromNode.id == nodeObject.id) {
    //             line.styleClass = "";
    //         } else {
    //             line.styleClass = "joubn";
    //         }
    //     });
    //     if (item.toNode.id == nodeObject.id || item.fromNode.id == nodeObject.id) {
    //         item.fromNode.opacity = 1;
    //         item.toNode.opacity = 1;
    //     }
    // });
    console.log('onNodeClick:', nodeObject);

    let ids: string[] = [nodeObject.id];
    for (const cNode of nodeObject.lot.childs) {
        ids.push(cNode.id);
    }

    const graphInstance = graphRef.value?.getInstance();
    if (graphInstance) {
        for (const node of graphInstance.getNodes()) {
            if (ids.includes(node.id)) {
                node.opacity = 1;
                node.color = 'rgb(116,2,173)';
            } else {
                node.opacity = 0.1;
                node.color = undefined;
            }
        }
        for (const link of graphInstance.getLinks()) {
            if (ids.includes(link.fromNode.id) && ids.includes(link.toNode.id)) {
                link.relations.forEach(line => {
                    line.color = 'rgb(116,2,173)';
                });
            } else {
                link.relations.forEach(line => {
                    line.color = '';
                });
            }
        }
    }

};

const onCanvasClick = ($event: RGUserEvent) => {
    console.log('onCanvasClick:', $event);
    // const graphInstance = graphRef.value?.getInstance();
    // if (graphInstance) {
    //     graphInstance.clearChecked();
    // }

    const graphInstance = graphRef.value?.getInstance();
    if (graphInstance) {
        for (const node of graphInstance.getNodes()) {
            node.opacity = 1;
            node.color = undefined;
        }
        for (const link of graphInstance.getLinks()) {
            link.relations.forEach(line => {
                line.color = undefined;
            });
        }
    }
};

const onLineClick = (lineObject: RGLine, linkObject: RGLink, $event: RGUserEvent) => {
    console.log('onLineClick:', lineObject);
};


const showGraph = async () => {
    const __graph_json_data: RGJsonData = {
        rootId: 'a',
        nodes: [
            { id: 'a', text: 'root' },
            { id: 'b', text: 'b' },
            { id: 'b1', text: 'b1' },
            { id: 'b1-1', text: 'b1-1' },
            { id: 'b1-2', text: 'b1-2' },
            { id: 'b1-3', text: 'b1-3' },
            { id: 'b1-4', text: 'b1-4' },
            { id: 'b1-5', text: 'b1-5' },
            { id: 'b1-6', text: 'b1-6' },
            { id: 'b2', text: 'b2' },
            { id: 'b2-1', text: 'b2-1' },
            { id: 'b2-2', text: 'b2-2' },
            { id: 'b2-3', text: 'b2-3' },
            { id: 'b2-4', text: 'b2-4' },
            { id: 'b3', text: 'b3' },
            { id: 'b3-1', text: 'b3-1' },
            { id: 'b3-2', text: 'b3-2' },
            { id: 'b3-3', text: 'b3-3' },
            { id: 'b3-4', text: 'b3-4' },
            { id: 'b3-5', text: 'b3-5' },
            { id: 'b3-6', text: 'b3-6' },
            { id: 'b3-7', text: 'b3-7' },
            { id: 'b4', text: 'b4' },
            { id: 'b4-1', text: 'b4-1' },
            { id: 'b4-2', text: 'b4-2' },
            { id: 'b4-3', text: 'b4-3' },
            { id: 'b4-4', text: 'b4-4' },
            { id: 'b4-5', text: 'b4-5' },
            { id: 'b4-6', text: 'b4-6' },
            { id: 'b4-7', text: 'b4-7' },
            { id: 'b4-8', text: 'b4-8' },
            { id: 'b4-9', text: 'b4-9' },
            { id: 'b5', text: 'b5' },
            { id: 'b5-1', text: 'b5-1' },
            { id: 'b5-2', text: 'b5-2' },
            { id: 'b5-3', text: 'b5-3' },
            { id: 'b5-4', text: 'b5-4' },
            { id: 'b6', text: 'b6' },
            { id: 'b6-1', text: 'b6-1' },
            { id: 'b6-2', text: 'b6-2' },
            { id: 'b6-3', text: 'b6-3' },
            { id: 'b6-4', text: 'b6-4' },
            { id: 'b6-5', text: 'b6-5' },
            { id: 'c', text: 'c' },
            { id: 'c1', text: 'c1' },
            { id: 'c1-1', text: 'c1-1' },
            { id: 'c1-2', text: 'c1-2' },
            { id: 'c1-3', text: 'c1-3' },
            { id: 'c1-4', text: 'c1-4' },
            { id: 'c1-5', text: 'c1-5' },
            { id: 'c1-6', text: 'c1-6' },
            { id: 'c1-7', text: 'c1-7' },
            { id: 'c2', text: 'c2' },
            { id: 'c2-1', text: 'c2-1' },
            { id: 'c2-2', text: 'c2-2' },
            { id: 'c3', text: 'c3' },
            { id: 'c3-1', text: 'c3-1' },
            { id: 'c3-2', text: 'c3-2' },
            { id: 'c3-3', text: 'c3-3' },
            { id: 'd', text: 'd' },
            { id: 'd1', text: 'd1' },
            { id: 'd1-1', text: 'd1-1' },
            { id: 'd1-2', text: 'd1-2' },
            { id: 'd1-3', text: 'd1-3' },
            { id: 'd1-4', text: 'd1-4' },
            { id: 'd1-5', text: 'd1-5' },
            { id: 'd1-6', text: 'd1-6' },
            { id: 'd1-7', text: 'd1-7' },
            { id: 'd1-8', text: 'd1-8' },
            { id: 'd2', text: 'd2' },
            { id: 'd2-1', text: 'd2-1' },
            { id: 'd2-2', text: 'd2-2' },
            { id: 'd3', text: 'd3' },
            { id: 'd3-1', text: 'd3-1' },
            { id: 'd3-2', text: 'd3-2' },
            { id: 'd3-3', text: 'd3-3' },
            { id: 'd3-4', text: 'd3-4' },
            { id: 'd3-5', text: 'd3-5' },
            { id: 'd4', text: 'd4' },
            { id: 'd4-1', text: 'd4-1' },
            { id: 'd4-2', text: 'd4-2' },
            { id: 'd4-3', text: 'd4-3' },
            { id: 'd4-4', text: 'd4-4' },
            { id: 'd4-5', text: 'd4-5' },
            { id: 'd4-6', text: 'd4-6' },
            { id: 'e', text: 'e' },
            { id: 'e1', text: 'e1' },
            { id: 'e1-1', text: 'e1-1' },
            { id: 'e1-2', text: 'e1-2' },
            { id: 'e1-3', text: 'e1-3' },
            { id: 'e1-4', text: 'e1-4' },
            { id: 'e1-5', text: 'e1-5' },
            { id: 'e1-6', text: 'e1-6' },
            { id: 'e2', text: 'e2' },
            { id: 'e2-1', text: 'e2-1' },
            { id: 'e2-2', text: 'e2-2' },
            { id: 'e2-3', text: 'e2-3' },
            { id: 'e2-4', text: 'e2-4' },
            { id: 'e2-5', text: 'e2-5' },
            { id: 'e2-6', text: 'e2-6' },
            { id: 'e2-7', text: 'e2-7' },
            { id: 'e2-8', text: 'e2-8' },
            { id: 'e2-9', text: 'e2-9' }
        ],
        lines: [
            { from: 'a', to: 'b' },
            { from: 'b', to: 'b1' },
            { from: 'b1', to: 'b1-1' },
            { from: 'b1', to: 'b1-2' },
            { from: 'b1', to: 'b1-3' },
            { from: 'b1', to: 'b1-4' },
            { from: 'b1', to: 'b1-5' },
            { from: 'b1', to: 'b1-6' },
            { from: 'b', to: 'b2' },
            { from: 'b2', to: 'b2-1' },
            { from: 'b2', to: 'b2-2' },
            { from: 'b2', to: 'b2-3' },
            { from: 'b2', to: 'b2-4' },
            { from: 'b', to: 'b3' },
            { from: 'b3', to: 'b3-1' },
            { from: 'b3', to: 'b3-2' },
            { from: 'b3', to: 'b3-3' },
            { from: 'b3', to: 'b3-4' },
            { from: 'b3', to: 'b3-5' },
            { from: 'b3', to: 'b3-6' },
            { from: 'b3', to: 'b3-7' },
            { from: 'b', to: 'b4' },
            { from: 'b4', to: 'b4-1' },
            { from: 'b4', to: 'b4-2' },
            { from: 'b4', to: 'b4-3' },
            { from: 'b4', to: 'b4-4' },
            { from: 'b4', to: 'b4-5' },
            { from: 'b4', to: 'b4-6' },
            { from: 'b4', to: 'b4-7' },
            { from: 'b4', to: 'b4-8' },
            { from: 'b4', to: 'b4-9' },
            { from: 'b', to: 'b5' },
            { from: 'b5', to: 'b5-1' },
            { from: 'b5', to: 'b5-2' },
            { from: 'b5', to: 'b5-3' },
            { from: 'b5', to: 'b5-4' },
            { from: 'b', to: 'b6' },
            { from: 'b6', to: 'b6-1' },
            { from: 'b6', to: 'b6-2' },
            { from: 'b6', to: 'b6-3' },
            { from: 'b6', to: 'b6-4' },
            { from: 'b6', to: 'b6-5' },
            { from: 'a', to: 'c' },
            { from: 'c', to: 'c1' },
            { from: 'c1', to: 'c1-1' },
            { from: 'c1', to: 'c1-2' },
            { from: 'c1', to: 'c1-3' },
            { from: 'c1', to: 'c1-4' },
            { from: 'c1', to: 'c1-5' },
            { from: 'c1', to: 'c1-6' },
            { from: 'c1', to: 'c1-7' },
            { from: 'c', to: 'c2' },
            { from: 'c2', to: 'c2-1' },
            { from: 'c2', to: 'c2-2' },
            { from: 'c', to: 'c3' },
            { from: 'c3', to: 'c3-1' },
            { from: 'c3', to: 'c3-2' },
            { from: 'c3', to: 'c3-3' },
            { from: 'a', to: 'd' },
            { from: 'd', to: 'd1' },
            { from: 'd1', to: 'd1-1' },
            { from: 'd1', to: 'd1-2' },
            { from: 'd1', to: 'd1-3' },
            { from: 'd1', to: 'd1-4' },
            { from: 'd1', to: 'd1-5' },
            { from: 'd1', to: 'd1-6' },
            { from: 'd1', to: 'd1-7' },
            { from: 'd1', to: 'd1-8' },
            { from: 'd', to: 'd2' },
            { from: 'd2', to: 'd2-1' },
            { from: 'd2', to: 'd2-2' },
            { from: 'd', to: 'd3' },
            { from: 'd3', to: 'd3-1' },
            { from: 'd3', to: 'd3-2' },
            { from: 'd3', to: 'd3-3' },
            { from: 'd3', to: 'd3-4' },
            { from: 'd3', to: 'd3-5' },
            { from: 'd', to: 'd4' },
            { from: 'd4', to: 'd4-1' },
            { from: 'd4', to: 'd4-2' },
            { from: 'd4', to: 'd4-3' },
            { from: 'd4', to: 'd4-4' },
            { from: 'd4', to: 'd4-5' },
            { from: 'd4', to: 'd4-6' },
            { from: 'a', to: 'e' },
            { from: 'e', to: 'e1' },
            { from: 'e1', to: 'e1-1' },
            { from: 'e1', to: 'e1-2' },
            { from: 'e1', to: 'e1-3' },
            { from: 'e1', to: 'e1-4' },
            { from: 'e1', to: 'e1-5' },
            { from: 'e1', to: 'e1-6' },
            { from: 'e', to: 'e2' },
            { from: 'e2', to: 'e2-1' },
            { from: 'e2', to: 'e2-2' },
            { from: 'e2', to: 'e2-3' },
            { from: 'e2', to: 'e2-4' },
            { from: 'e2', to: 'e2-5' },
            { from: 'e2', to: 'e2-6' },
            { from: 'e2', to: 'e2-7' },
            { from: 'e2', to: 'e2-8' },
            { from: 'e2', to: 'e2-9' }
        ]
    };

    const graphInstance = graphRef.value.getInstance();
    if (graphInstance) {
        await graphInstance.setJsonData(__graph_json_data);
        await graphInstance.moveToCenter();
        await graphInstance.zoomToFit();
        // await graphInstance.setZoom(10);
    }
};

</script>

<style scoped></style>


<style lang="scss">
.my-graph {
    background: linear-gradient(to right, rgb(16, 185, 129), rgb(101, 163, 13));
}


.joubn {
    opacity: .1;
}

.joubn+g {
    opacity: 0;
}

// 通过全局样式 修改图谱内部使用到的 自定义样式
.my-line-style-1 {
    .c-rg-line-checked {
        animation: my-line-anm1 2s linear infinite;
    }

    width:1000px;
    height: 800px;
}

.my-line-style-2 {
    .c-rg-line-checked {
        animation: my-line-anm2 1s infinite;
    }
}

.my-line-style-3 {
    .c-rg-line-checked {
        animation: my-line-anm3 1s infinite;
    }
}

.my-line-style-4 {
    .c-rg-line-checked {
        animation: my-line-anm4 1s infinite;
    }
}

@keyframes my-line-anm1 {
    0% {
        stroke-dashoffset: 100px;
        stroke-dasharray: 5, 5, 5;
    }

    100% {
        stroke-dasharray: 5, 5, 5;
        stroke-dashoffset: 3px;
    }
}

@keyframes my-line-anm2 {
    from {
        stroke-dashoffset: 0;
        stroke-dasharray: 4, 4, 4;
    }

    to {
        stroke-dashoffset: 10px;
        stroke-dasharray: 20, 20, 20;
    }
}

@keyframes my-line-anm3 {
    0% {
        stroke-opacity: 1;
    }

    50% {
        stroke-opacity: 0.2;
    }

    100% {
        stroke-opacity: 1;
    }
}

@keyframes my-line-anm4 {
    0% {
        stroke-dasharray: 0, 100%;
    }

    100% {
        stroke-dasharray: 100%, 0;
    }
}
</style>