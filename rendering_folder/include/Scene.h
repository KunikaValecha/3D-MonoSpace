#pragma once

#include <stdio.h>
#include <string.h>
#include <cmath>
#include <vector>
#include <string>
#include <sstream>

#include <GL/glew.h>
#include <GLFW/glfw3.h>

#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>

#include "../include/CommonValues.h"
#include "../include/Window.h"
#include "../include/Mesh.h"
#include "../include/Shader.h"
#include "../include/Camera.h"
#include "../include/Texture.h"
#include "../include/DirectionalLight.h"
#include "../include/PointLight.h"
#include "../include/SpotLight.h"
#include "../include/Material.h"
#include "../include/Model.h"

struct ModelInputParams
{
    std::string label;
    float x, y, z, xscale, yscale, zscale, xrot, yrot, zrot;

    ModelInputParams(std::string l, 
                    float p_x, float p_y, float p_z, 
                    float p_xscale, float p_yscale, float p_zscale, 
                    float p_xrot, float p_yrot, float p_zrot)
    {
        label = l;
        x = p_x;
        y = p_y;
        z = p_z;
        xscale = p_xscale;
        yscale = p_yscale;
        zscale = p_zscale;
        xrot = p_xrot;
        yrot = p_yrot;
        zrot = p_zrot;
    }
};

class Scene
{
public:
    Window mainWindow;
    std::vector<Mesh*> meshList;
    std::vector<Shader> shaderList;
    Shader directionalShadowShader;
    Shader omniShadowShader;

    std::vector<Model> modelList;
    Material shinyMaterial, dullMaterial;
    Model bishop, king, queen, rook, knight, pawn;	

    Camera camera;

    Texture brickTexture;
    Texture marbleTexture;
    Texture plainTexture;
    
    DirectionalLight mainLight;
    PointLight pointLights[MAX_POINT_LIGHTS];
    SpotLight spotLights[MAX_SPOT_LIGHTS];

    GLfloat deltaTime;
    GLfloat lastTime;

    glm::mat4 projection;

    unsigned int pointLightCount, spotLightCount;

    GLuint uniformProjection, uniformModel, uniformView, uniformEyePosition, uniformSpecularIntensity, uniformShininess, uniformFogColour, uniformColour,
           uniformDirectionalLightTransform, uniformOmniLightPos, uniformFarPlane;

    Scene();
    Scene(char* fileName);

    void Init();
    void InitFromFile(char* fileName);

    void calcAverageNormals(unsigned int * indices, unsigned int indiceCount, GLfloat * vertices, unsigned int verticeCount, 
						unsigned int vLength, unsigned int normalOffset);
    void CreateObjects();
    void CreateShaders();

    void OmniShadowMapPass(PointLight* light);

    void TransformAndRenderModel(Model* m, Material* mat, GLfloat transX, GLfloat transY, GLfloat transZ, GLfloat scale, GLfloat rotX, GLfloat rotY, GLfloat rotZ);
    void TransformAndRenderModel(Model* m, Material* mat, GLfloat transX, GLfloat transY, GLfloat transZ, GLfloat scaleX, GLfloat scaleY, GLfloat scaleZ, GLfloat rotX, GLfloat rotY, GLfloat rotZ);

    void TransformAndRenderMesh(Mesh* m, Material* mat, GLfloat transX, GLfloat transY, GLfloat transZ, GLfloat scale, GLfloat rotX, GLfloat rotY, GLfloat rotZ);
    void RenderScene();
    void DirectionalShadowMapPass();
    void RenderPass(glm::mat4 viewMatrix);
    void Render();
};