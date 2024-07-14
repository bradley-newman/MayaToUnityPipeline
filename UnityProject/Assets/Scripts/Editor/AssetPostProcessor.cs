using UnityEngine;
using UnityEditor;
using System.Collections.Generic;
using System.Web;

namespace UnitEditorPipeline
{
    public static class ModelData
    {
        public static Dictionary<string, object> userProperties = new Dictionary<string, object>();
        public const string AssetTypeKey = "asset_type";
        public struct AssetTypes
        {
            public const string Mesh = "Mesh";
            public const string Animation = "Animation";
        }

        public static string AssetType
        {
            get
            {
                if (userProperties.TryGetValue(AssetTypeKey, out object value))
                {
                    return value.ToString();
                }
                else
                {
                    return string.Empty;
                }
            }
        }

        public static class MeshProperties
        {
            private const string StaticKey = "static";
            public static bool Static
            {
                get
                {
                    if (userProperties.TryGetValue(StaticKey, out object value))
                    {
                        return (bool)value;
                    }
                    else
                    {
                        return false;
                    }
                }
            }
        }

        public static class AnimationProperties
        {
            public const string LoopKey = "loop";
            public static bool Loop
            {
                get
                {
                    if (userProperties.TryGetValue(LoopKey, out object value))
                    {
                        return (bool)value;
                    }
                    else
                    {
                        return false;
                    }
                }
            }
        }
    }

    public class AssetPostProcessor : AssetPostprocessor
    {
        private bool checked_first_object = false;

        void OnPreprocessModel()
        {
            ModelImporter modelImporter = assetImporter as ModelImporter;
            modelImporter.materialImportMode = ModelImporterMaterialImportMode.None;
        }

        void OnPostprocessGameObjectWithUserProperties(GameObject go, string[] propNames, object[] values)
        {
            //Parse the Maya Extra Attributes (i.e. User Properties) in the FBX.     
            //We're only interested in the first root gameobject in the FBX hierarchy (where the Extra Attributes were added in Maya)
            if (checked_first_object)
            {
                return;
            }

            checked_first_object = true;

            ModelData.userProperties.Clear();

            //The first property is the Asset Type
            if (propNames[0] == ModelData.AssetTypeKey)
            {
                for (int i = 0; i < propNames.Length; i++)
                {
                    ModelData.userProperties.Add(propNames[i], values[i]);
                }
            }
        }

        void OnPreprocessAnimation()
        {
            if (ModelData.AssetType == ModelData.AssetTypes.Animation)
            {
                ModelImporter modelImporter = assetImporter as ModelImporter;
                Debug.Log($"PreProcessingAnimation for {modelImporter.assetPath}");
                ModelImporterClipAnimation[] clipAnimations = modelImporter.defaultClipAnimations;

                for (int i = 0; i < clipAnimations.Length; i++)
                {
                    bool loop = ModelData.AnimationProperties.Loop;

                    if (loop)
                    {
                        Debug.Log($"- Setting clip: {clipAnimations[i].name}.loopTime = {loop}");
                        clipAnimations[i].loopTime = loop;
                    }
                }

                modelImporter.clipAnimations = clipAnimations;
                modelImporter.SaveAndReimport();
            }
        }
    }
}