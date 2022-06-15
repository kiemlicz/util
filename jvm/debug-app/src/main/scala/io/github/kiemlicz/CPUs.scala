package io.github.kiemlicz

object CPUs {
  def main(args: Array[String]): Unit = {
    println(s"#CPUs: ${Runtime.getRuntime.availableProcessors()}")
  }
}
