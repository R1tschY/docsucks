#include <map>
#include <string>
#include <memory>
#include <boost/core/demangle.hpp>
#include <sstream>

namespace MyModule {

class Service
{
public:
  virtual ~Service() {}
};

/**
 * a service locator for your services
 *
 * \code
 * struct AnswerService : Service {
 *   virtual int getAnswer() { return 42; }
 * };
 * auto locator = ServiceLocator();
 * locator.set("TruthService", std::unique_ptr<AnswerService>(new AnswerService()));
 * std::cout << locator.get<AnswerService>("TruthService")->getAnswer() << '\n';
 * \endcode
 *
 * \verbatim
 * 42
 * \endverbatim
 *
 * \code
 * std::cout << locator.get<AnswerService>("TruthService") << '\n';
 * \endcode
 * \verbatim
 * 0
 * \endverbatim
 */
class ServiceLocator
{
public:
  ServiceLocator() { }

  void set(const std::string& name, std::unique_ptr<Service> service)
  {
    services_[name] = std::move(service);
  }

  template<typename T>
  T* get(const std::string& name)
  {
    auto iter = services_.find(name);
    if (iter == services_.end())
      return nullptr;

    Service* ptr = iter->second.get();
    if (!ptr)
      return nullptr;

    T* tptr = dynamic_cast<T*>(ptr);
    if (!tptr)
    {
      std::ostringstream stream;
      stream
        << "wrong service type: expected "
        << boost::core::demangle(typeid(T).name())
        << " got "
        << boost::core::demangle(typeid(ptr).name());
      throw std::runtime_error(stream.str());
    }

    return tptr;
  }


private:
  std::map<std::string, std::unique_ptr<Service>> services_;
};

} // namespace MyModule
