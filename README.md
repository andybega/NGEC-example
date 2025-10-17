# NGEC-like testing package

This is a minimal Python package that has some of the most important NGEC 
dependencies, like vllm, torch, and spacy. 

It includes some helper functions that can be used to check for the availability 
of a GPU (on Linux, Windows), or MPS support (on Apple Sillicon), as well as
whether vLLM is importable:

```python
import NGECx

NGECx.gpu_available()
NGECx.mps_available()
NGECx.vllm_importable()
```