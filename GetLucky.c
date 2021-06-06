#include "python.h" 

static PyObject*
GetLuckyNumber(PyObject* self, PyObject* args)
{
    int inum, iage;

    if (!PyArg_ParseTuple(args, "ii", &inum, &iage))
        return NULL;

    FILE* fp = NULL;
    fopen_s(&fp, "PredictSet.txt", "r");
    if (fp == NULL) return 0;

    int numval=0, ageval=0;
    while (!feof(fp)) {
        int top1, top2, top3;
        int age, num;
        char* sex = NULL;

        fscanf(fp, "%d %d %d %d %d \n", &top1, &top2, &top3, &age, &num);

        if (inum == num) {
            numval += top1 + top2 + top3;
        }
        if (iage == age) {
            ageval += top1 + top2 + top3;
        }
    }
    fclose(fp);
    int returnval = numval + ageval;
    return Py_BuildValue("i", returnval);
}

static PyMethodDef GetLuckyMethods[] = {
    {"GetLuckyNumber", GetLuckyNumber, METH_VARARGS,
    "Get lucky number of next racing"},
    {NULL, NULL, 0, NULL}    //배열의 끝을 나타낸다.
};


static struct PyModuleDef GetLuckymodule = {
    PyModuleDef_HEAD_INIT,
    "GetLucky",            // 모듈 이름
    "For Predict Horse-Racing using RandomForest", // 모듈 설명을 적는 부분, 모듈의 __doc__에 저장됩니다.
    -1,GetLuckyMethods
};

PyMODINIT_FUNC
PyInit_GetLucky(void)
{
    return PyModule_Create(&GetLuckymodule);
}
