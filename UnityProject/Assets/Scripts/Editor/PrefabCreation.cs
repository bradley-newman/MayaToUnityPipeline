using System.IO;
using UnityEngine;
using UnityEditor;

namespace UnitEditorPipeline
{
    public static class PrefabCreation
    {
        [MenuItem("Assets/Create Mesh Prefab")]
        public static void CreateMeshPrefabMenuItem()
        {
            Object[] selectedAssets = Selection.GetFiltered(typeof(Object), SelectionMode.Assets);
            CreateMeshPrefab(selectedAssets[0]);
        }

        public static void CreateMeshPrefab(Object fbxAsset)
        {
            string fbxPath = AssetDatabase.GetAssetPath(fbxAsset);
            Debug.Log($"Importing: {fbxPath}");
            AssetDatabase.ImportAsset(fbxPath);

            if (ModelData.AssetType == ModelData.AssetTypes.Mesh)
            {
                string prefabPath = CreatePrefab(fbxAsset);

                if (ModelData.MeshProperties.Static)
                {
                    Debug.Log($"{fbxPath} is a static mesh.");
                    SetStatic(prefabPath);
                }
            }
        }

        private static string CreatePrefab(Object fbxAsset)
        {
            string fbxPath = AssetDatabase.GetAssetPath(fbxAsset);
            GameObject fbxMainAsset = (GameObject)AssetDatabase.LoadMainAssetAtPath(fbxPath);
            string prefabName = $"{fbxMainAsset.name}_PFB";
            GameObject prefabRootGO = new GameObject(prefabName);
            string prefabPath = Path.Combine(Path.GetDirectoryName(fbxPath), prefabRootGO.name + ".prefab");
            PrefabUtility.SaveAsPrefabAssetAndConnect(prefabRootGO, prefabPath, InteractionMode.AutomatedAction);

            //Edit the Prefab to put the FBX inside it
            using (var editingScope = new PrefabUtility.EditPrefabContentsScope(prefabPath))
            {
                var prefabRoot = editingScope.prefabContentsRoot;
                GameObject instantiatedFbx = PrefabUtility.InstantiatePrefab(fbxMainAsset) as GameObject;
                instantiatedFbx.transform.parent = prefabRoot.transform;
            }

            Object.DestroyImmediate(prefabRootGO);

            Debug.Log("Created prefab: " + prefabPath);
            return prefabPath;
        }

        private static void SetStatic(string prefabPath)
        {
            using (var editingScope = new PrefabUtility.EditPrefabContentsScope(prefabPath))
            {
                var flags = StaticEditorFlags.ContributeGI
                            | StaticEditorFlags.OccluderStatic
                            | StaticEditorFlags.BatchingStatic
                            | StaticEditorFlags.OccludeeStatic
                            | StaticEditorFlags.ReflectionProbeStatic;

                var prefabRoot = editingScope.prefabContentsRoot;
                Transform[] allChildren = prefabRoot.transform.GetComponentsInChildren<Transform>();

                foreach (Transform child in allChildren)
                {
                    if (child.GetComponent<Renderer>())
                    {
                        GameObjectUtility.SetStaticEditorFlags(child.gameObject, flags);
                    }
                }
            }
        }
    }
}