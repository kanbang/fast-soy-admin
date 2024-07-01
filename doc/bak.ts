
interface ITreeItem {
    id: number;
    parent_id: number | null;
    children?: ITreeItem[];
}

function generateTree(items: ITreeItem[]): ITreeItem[] {
    const treeItemMap: { [key: number]: ITreeItem } = {};
    const tree: ITreeItem[] = [];

    // 建立 ID 到 item 的映射
    items.forEach(item => {
        treeItemMap[item.id] = item;
    });

    // 构建树结构
    items.forEach(item => {
        if (item.parent_id !== null && item.parent_id !== 0) {
            const parent = treeItemMap[item.parent_id];
            if (parent) {
                if (!parent.children) {
                    parent.children = [];
                }
                parent.children.push(treeItemMap[item.id]);
            }
        } else {
            tree.push(treeItemMap[item.id]);
        }
    });

    return tree;
}



function handleClick(equipid) {
    // routerPushByKey('early-warning_monitor', { query: { a: '1' } })
    // routerPushByKey('early-warning_monitor', { params: { a: '1' } })
    // <NButton @click="routerPushByKey('early-warning_monitor', { query: { a: '1' } })">
}